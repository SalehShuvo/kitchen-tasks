
(define
  (problem none_250713_185845_1)
  (:domain domain)

  (:objects
	base
	base-torso
	head
	left_arm
	left_gripper
	minifridge
	minifridge::link_2
	right_arm
	right_gripper
	sink_counter_right
	torso
	veggiecabbage
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

	(edible veggiecabbage)

	(graspable veggiecabbage)

	(space minifridge::link_2)

	(region minifridge::link_2)

	(oftype veggiecabbage @edible)

	(staticlink sink_counter_right)
	(staticlink minifridge::link_2)

	(bconf q368=(1.615, 0.425, 0.678, 1.102))

	(atbconf q368=(1.615, 0.425, 0.678, 1.102))

	(stackable veggiecabbage sink_counter_right)

	(containable veggiecabbage minifridge::link_2)

	(pose veggiecabbage p393=(0.599, 0.578, 1.095, 0.0, -0.0, 1.126))

	(atpose veggiecabbage p393=(0.599, 0.578, 1.095, 0.0, -0.0, 1.126))

	(aconf left aq408=(1.321, 0.637, -0.344, -1.059, -2.846, -1.948, -2.8))
	(aconf right aq360=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))

	(ataconf left aq408=(1.321, 0.637, -0.344, -1.059, -2.846, -1.948, -2.8))
	(ataconf right aq360=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))

	(supported veggiecabbage p393=(0.599, 0.578, 1.095, 0.0, -0.0, 1.126) sink_counter_right)

  )

  (:goal (and
    (in veggiecabbage minifridge::link_2)
  ))
)
        