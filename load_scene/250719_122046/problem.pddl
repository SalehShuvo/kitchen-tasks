
(define
  (problem none_250719_122046_1)
  (:domain domain)

  (:objects
	base
	base-torso
	head
	left_arm
	left_gripper
	minifridge
	minifridge::joint_0
	right_arm
	right_gripper
	torso
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

	(staticlink minifridge)

	(door minifridge::joint_0)

	(joint minifridge::joint_0)

	(unattachedjoint minifridge::joint_0)

	(bconf q328=(1.61, 7.544, 0.394, 3.826))

	(position minifridge::joint_0 pstn39=0.0)

	(atbconf q328=(1.61, 7.544, 0.394, 3.826))
	(isjointto minifridge::joint_0 minifridge)

	(atposition minifridge::joint_0 pstn39=0.0)

	(isclosedposition minifridge::joint_0 pstn39=0.0)

	(aconf left aq280=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))
	(aconf right aq376=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))

	(ataconf left aq280=(0.677, -0.343, 1.2, -1.467, 1.242, -1.954, 2.223))
	(ataconf right aq376=(-2.135, 1.296, -3.75, -0.15, -10000.0, -0.1, -10000.0))

  )

  (:goal (and
    (openedjoint minifridge::joint_0)
  ))
)
        