from __future__ import print_function

import time

from collections import Counter
from itertools import product
from copy import deepcopy, copy

from pddlstream.algorithms.instantiation import Instantiator
from pddlstream.algorithms.scheduling.plan_streams import plan_streams, OptSolution
from pddlstream.algorithms.scheduling.recover_streams import evaluations_from_stream_plan
from pddlstream.algorithms.constraints import add_plan_constraints, PlanConstraints, WILD
from pddlstream.language.constants import FAILED, INFEASIBLE, is_plan
from pddlstream.language.conversion import evaluation_from_fact, substitute_expression
from pddlstream.language.function import FunctionResult, Function
from pddlstream.language.stream import StreamResult, Result
from pddlstream.language.statistics import check_effort, compute_plan_effort
from pddlstream.language.object import Object, OptimisticObject
from pddlstream.utils import INF, safe_zip, get_mapping, implies, elapsed_time

CONSTRAIN_STREAMS = False
CONSTRAIN_PLANS = False
MAX_DEPTH = INF # 1 | INF

def is_refined(stream_plan):
    # TODO: lazily expand the shared objects in some cases to prevent increase in size
    if not is_plan(stream_plan):
        return True
    # TODO: some of these opt_index equal None
    return all((result.opt_index is None) or result.is_refined()
               for result in stream_plan)

##################################################

def optimistic_process_instance(instantiator, instance, verbose=False):
    for result in instance.next_optimistic():
        if verbose:
            print(result) # TODO: make a debug tools that reports the optimistic streams
        new_facts = False
        complexity = instantiator.compute_complexity(instance)
        for fact in result.get_certified():
            new_facts |= instantiator.add_atom(evaluation_from_fact(fact), complexity)
        if isinstance(result, FunctionResult) or new_facts:
            yield result

def prune_high_effort_streams(streams, max_effort=INF, **effort_args):
    # TODO: convert streams to test streams with extremely high effort
    low_effort_streams = []
    for stream in streams:
        effort = stream.get_effort(**effort_args)
        if isinstance(stream, Function) or check_effort(effort, max_effort):
            low_effort_streams.append(stream)
    return low_effort_streams

def optimistic_process_streams(evaluations, streams, complexity_limit=INF, verbose=True, **effort_args):
    from pybullet_tools.logging_utils import myprint as print
    optimistic_streams = prune_high_effort_streams(streams, **effort_args)
    instantiator = Instantiator(optimistic_streams)
    for evaluation, node in evaluations.items():
        if node.complexity <= complexity_limit:
            instantiator.add_atom(evaluation, node.complexity)
    results = []
    while instantiator and (instantiator.min_complexity() <= complexity_limit):
        results.extend(optimistic_process_instance(instantiator, instantiator.pop_stream()))
        # TODO: instantiate and solve to avoid repeated work
    exhausted = not instantiator
    if verbose:
        from pybullet_planning.pybullet_tools.logging_utils import myprint
        stream_frequencies = Counter(result.external.name for result in results)
        myprint(f'Optimistic streams: {stream_frequencies}')
        print('Exhausted optimistic:', exhausted)
    return results, exhausted

##################################################

def optimistic_stream_instantiation(instance, bindings, opt_evaluations, only_immediate=False):
    # TODO: combination for domain predicates
    new_instances = []
    input_candidates = [bindings.get(i, [i]) for i in instance.input_objects]
    if only_immediate and not all(len(candidates) == 1 for candidates in input_candidates):
        return new_instances
    for input_combo in product(*input_candidates):
        mapping = get_mapping(instance.input_objects, input_combo)
        domain_evaluations = set(map(evaluation_from_fact, substitute_expression(
            instance.get_domain(), mapping))) # TODO: could just instantiate first
        if domain_evaluations <= opt_evaluations:
            new_instance = instance.external.get_instance(input_combo)
            # TODO: method for eagerly evaluating some of these?
            if not new_instance.is_refined():
                new_instance.refine()
            new_instances.append(new_instance)
    return new_instances

def optimistic_stream_evaluation(evaluations, stream_plan, use_bindings=True):
    # TODO: can also use the instantiator and operate directly on the outputs
    # TODO: could bind by just using new_evaluations
    evaluations = set(evaluations) # Converts to a set for subset testing
    opt_evaluations = set(evaluations)
    new_results = []
    bindings = {} # TODO: report the depth considered
    #if is_refined(stream_plan):
    #    return new_results, bindings
    for opt_result in stream_plan: # TODO: just refine the first step of the plan
        for new_instance in optimistic_stream_instantiation(
                opt_result.instance, (bindings if use_bindings else {}), opt_evaluations):
            for new_result in new_instance.next_optimistic():
                opt_evaluations.update(map(evaluation_from_fact, new_result.get_certified()))
                new_results.append(new_result)
                if isinstance(new_result, StreamResult): # Could not add if same value
                    for opt, obj in safe_zip(opt_result.output_objects, new_result.output_objects):
                        bindings.setdefault(opt, []).append(obj)
    return new_results, bindings

##################################################

# def compute_stream_results(evaluations, opt_results, externals, complexity_limit, **effort_args):
#     # TODO: revisit considering double bound streams
#     functions = list(filter(lambda s: type(s) is Function, externals))
#     opt_evaluations = evaluations_from_stream_plan(evaluations, opt_results)
#     new_results, _ = optimistic_process_streams(opt_evaluations, functions, complexity_limit, **effort_args)
#     return opt_results + new_results

def compute_skeleton_constraints(opt_plan, bindings):
    skeleton = []
    groups = {arg: values for arg, values in bindings.items() if len(values) != 1}
    action_plan, preimage_facts = opt_plan
    for name, args in action_plan:
        new_args = []
        for arg in args:
            if isinstance(arg, Object):
                new_args.append(arg)
            elif isinstance(arg, OptimisticObject):
                new_args.append(WILD)
                # TODO: might cause some strange effects on continuous_tamp -p blocked
                #assert bindings.get(arg, [])
                #if len(bindings[arg]) == 1:
                #    new_args.append(bindings[arg][0])
                #else:
                #    #new_args.append(WILD)
                #    new_args.append(arg)
            else:
                raise ValueError(arg)
        skeleton.append((name, new_args))
    # exact=False because we might need new actions
    return PlanConstraints(skeletons=[skeleton], groups=groups, exact=False, max_cost=INF)

def get_optimistic_solve_fn(goal_exp, domain, negative, max_cost=INF, **kwargs):
    # TODO: apply to hierarchical actions representations (will need to instantiate more actions)
    def fn(evaluations, results, constraints):
        if constraints is None:
            return plan_streams(evaluations, goal_exp, domain, results, negative,
                                max_cost=max_cost, **kwargs)
        #print(*relaxed_stream_plan(evaluations, goal_exp, domain, results, negative,
        #                               max_cost=max_cost, **kwargs))
        #constraints.dump()
        domain2 = deepcopy(domain)
        evaluations2 = copy(evaluations)
        goal_exp2 = add_plan_constraints(constraints, domain2, evaluations2, goal_exp, internal=True)
        max_cost2 = max_cost if (constraints is None) else min(max_cost, constraints.max_cost)
        return plan_streams(evaluations2, goal_exp2, domain2, results, negative,
                            max_cost=max_cost2, **kwargs)
    return fn

##################################################

def hierarchical_plan_streams(evaluations, externals, results, optimistic_solve_fn, complexity_limit,
                              depth, constraints, **effort_args): # refine_all=False
    if MAX_DEPTH <= depth:
        return [], depth
    solutions = optimistic_solve_fn(evaluations, results, constraints)
    if all(is_refined(stream_plan) for stream_plan, _, _ in solutions):
        return solutions, depth

    #action_plan, preimage_facts = opt_plan
    #dump_plans(stream_plan, action_plan, cost)
    #create_visualizations(evaluations, stream_plan, depth)
    #print(depth, get_length(stream_plan))
    #print('Stream plan ({}, {:.3f}): {}\nAction plan ({}, {:.3f}): {}'.format(
    #    get_length(stream_plan), compute_plan_effort(stream_plan), stream_plan,
    #    get_length(action_plan), cost, str_from_plan(action_plan)))
    #if is_plan(stream_plan):
    #    for result in stream_plan:
    #        effort = compute_result_effort(result, unit_efforts=True)
    #        if effort != 0:
    #            print(result, effort)
    #print()

    # TODO: identify control parameters that can be separated across actions
    refined_solutions = []
    for solution in solutions:
        stream_plan, _, _ = solution
        if not is_refined(stream_plan):
            optimistic_stream_evaluation(evaluations, stream_plan)
        # else:
        #     refined_solutions.append(solution)
    #if refine_all and (len(refined_solutions) != len(solutions)):
    #    refined_solutions.clear()

    new_depth = depth + 1 # TODO: need to handle depth to use refined_solutions
    if not (CONSTRAIN_STREAMS or CONSTRAIN_PLANS):
        return refined_solutions, new_depth
    #if CONSTRAIN_STREAMS:
    #    next_results = compute_stream_results(evaluations, new_results, externals, complexity_limit, **effort_args)
    #else:
    next_results, _ = optimistic_process_streams(evaluations, externals, complexity_limit, **effort_args)
    next_constraints = None
    if CONSTRAIN_PLANS:
        raise NotImplementedError()
        next_constraints = compute_skeleton_constraints(opt_plan, bindings)
    return hierarchical_plan_streams(evaluations, externals, next_results, optimistic_solve_fn, complexity_limit,
                                     new_depth, next_constraints, **effort_args)

def iterative_plan_streams(all_evaluations, externals, optimistic_solve_fn, complexity_limit, save_streams_txt=False,
                           **effort_args):
    # Previously didn't have unique optimistic objects that could be constructed at arbitrary depths
    start_time = time.time()
    complexity_evals = {e: n for e, n in all_evaluations.items() if n.complexity <= complexity_limit}
    num_iterations = 0
    timeout = 2 * 60
    timeout = 5 * 60
    last_result = None
    while True:
        num_iterations += 1
        results, exhausted = optimistic_process_streams(complexity_evals, externals, complexity_limit, **effort_args)

        # ----------- added by Yang to see optimistic streams -----------
        if save_streams_txt:
            summarize_results(results, complexity_limit, num_iterations)  ## added by Yang
            if last_result == len(results):
                last_result = len(results)
                print('num_iterations', num_iterations, len(results))
                continue
            last_result = len(results)

        opt_solutions, final_depth = hierarchical_plan_streams(
            complexity_evals, externals, results, optimistic_solve_fn, complexity_limit,
            depth=0, constraints=None, **effort_args)
        print('Attempt: {} | Results: {} | Depth: {} | Solutions: {} | Time: {:.3f}'.format(
            num_iterations, len(results), final_depth, len(opt_solutions), elapsed_time(start_time)))
        if opt_solutions:
            return opt_solutions

        if final_depth == 0 or (time.time() - start_time > timeout):
            if time.time() - start_time > timeout:
                print(f'iterative_plan_streams.timeout = {timeout}')
            status = INFEASIBLE if exhausted else opt_solutions
            return status

    # TODO: should streams along the sampled path automatically have no optimistic value


def summarize_results(results, complexity_limit, num_iterations):
    from os.path import join, isdir
    from os import mkdir
    from datetime import datetime

    summary = {}
    for result in results:
        name = result.name
        obj = result.input_objects[0].value
        if name not in summary:
            summary[name] = {}
        if obj not in summary[name]:
            summary[name][obj] = []
        summary[name][obj].append(result)

    abstract = {}
    for k, v in summary.items():
        for kk, vv in v.items():
            key = f'{k}({kk}, ...)'
            abstract[key] = (len(vv), vv[0])
    abstract = {k: v for k, v in sorted(abstract.items(), key=lambda item: item[1][0], reverse=True)}
    abstract_full = '\n'.join([f'    {v[0]} \t {k}  |  e.g. {v[1]}' for k,v in abstract.items()])
    abstract_filtered = '\n'.join([f'    {v[0]} \t {k}  |  e.g. {v[1]}' for k,v in abstract.items() if v[0]>=3])
    headline = f'COMPLEXITY: {complexity_limit}  |  ATTEMPT: {num_iterations}   |  RESULTS: {len(results)} \n\n'

    folder = join('visualizations', 'stream_results')
    if not isdir(folder): mkdir(folder)
    now = datetime.now().strftime("%m%d-%H%M%S")
    with open(join(folder, f'{now}_{complexity_limit}_{num_iterations}.txt'), 'w') as f:
        f.write(abstract_full)
        f.write(headline)
        f.write('\n\n-----------------------------------\n\n')
        f.write('\n'.join([str(r) for r in results]))

    with open(join(folder, f'stream_results.txt'), 'a') as f:
        f.write(headline)
        f.write(abstract_filtered)
        f.write('\n\n-----------------------------------\n\n')
