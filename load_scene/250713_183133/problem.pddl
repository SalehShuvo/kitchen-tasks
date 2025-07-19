
(define
  (problem none_250713_183133_1)
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
	veggiepotato
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

	(edible veggiepotato)

	(staticlink counter#1)

	(graspable veggiepotato)

	(oftype veggiepotato @edible)

	(stackable veggiepotato counter#1)

	(bconf q600=(1.124, 2.62, 0.991, 0.702))

	(atbconf q600=(1.124, 2.62, 0.991, 0.702))

	(pose veggiepotato p221=(0.459, 3.066, 1.12, 0.0, -0.0, 2.581))

	(atpose veggiepotato p221=(0.459, 3.066, 1.12, 0.0, -0.0, 2.581))

	(ataconf left aq280=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))
	(ataconf right aq560=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))

	(aconf right aq560=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))
	(aconf left aq280=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))

	(supported veggiepotato p221=(0.459, 3.066, 1.12, 0.0, -0.0, 2.581) counter#1)

  )

  (:goal (and
    (holding left veggiepotato)
  ))
)
        