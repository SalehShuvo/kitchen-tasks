
(define
  (problem none_250705_174010_1)
  (:domain domain)

  (:objects
	base
	base-torso
	head
	left_arm
	left_gripper
	right_arm
	right_gripper
	sink_counter_left
	torso
	veggietomato
  )

  (:init
	;; discrete facts (e.g. types, affordances)
	(canmove)
	(canpick)

	(arm left)

	(canmovebase)

	(canpull left)

	(cangrasphandle)
	(handempty left)

	(controllable left)

	(edible veggietomato)

	(graspable veggietomato)

	(oftype veggietomato @edible)

	(staticlink sink_counter_left)

	(bconf q528=(1.139, 2.077, 0.623, 2.362))

	(stackable veggietomato sink_counter_left)

	(atbconf q528=(1.139, 2.077, 0.623, 2.362))

	(pose veggietomato p211=(0.614, 1.563, 1.102, 0.0, -0.0, 2.897))

	(atpose veggietomato p211=(0.614, 1.563, 1.102, 0.0, -0.0, 2.897))

	(aconf right aq384=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))
	(aconf left aq240=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))

	(ataconf right aq384=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))
	(ataconf left aq240=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))

	(supported veggietomato p211=(0.614, 1.563, 1.102, 0.0, -0.0, 2.897) sink_counter_left)

  )

  (:goal (and
    (holding left veggietomato)
  ))
)
        