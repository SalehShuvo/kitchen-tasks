
(define
  (problem none_250719_163931_1)
  (:domain domain)

  (:objects
	base
	base-torso
	counter#1
	head
	left_arm
	left_gripper
	right_arm
	right_gripper
	torso
	veggiezucchini
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

	(staticlink counter#1)

	(edible veggiezucchini)

	(graspable veggiezucchini)

	(oftype veggiezucchini @edible)

	(stackable veggiezucchini counter#1)

	(bconf q0=(1.168, 1.439, 0.841, 1.297))

	(atbconf q0=(1.168, 1.439, 0.841, 1.297))

	(pose veggiezucchini p239=(0.375, 1.635, 1.079, 0.0, -0.0, 2.511))

	(atpose veggiezucchini p239=(0.375, 1.635, 1.079, 0.0, -0.0, 2.511))

	(aconf left aq424=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))
	(aconf right aq144=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))

	(ataconf left aq424=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))
	(ataconf right aq144=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))

	(supported veggiezucchini p239=(0.375, 1.635, 1.079, 0.0, -0.0, 2.511) counter#1)

  )

  (:goal (and
    (holding left veggiezucchini)
  ))
)
        