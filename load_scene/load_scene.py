import config
import pickle
from pybullet_planning.lisdf_tools.lisdf_loader import load_lisdf_pybullet
from pybullet_planning.world_builder.world import State
# from pybullet_planning.pybullet_tools.pr2_primitives import apply_commands
from pybullet_planning.world_builder.actions import apply_commands
from pybullet_planning.pybullet_tools.utils import disconnect, LockRenderer, has_gui, WorldSaver, wait_if_gui, \
    SEPARATOR, get_aabb, wait_for_duration, has_gui, reset_simulation, set_random_seed, \
    set_numpy_seed, set_renderer

lisdf_path = '250719_163931/scene.lisdf'
world = load_lisdf_pybullet(lisdf_path)
state = State(world)
with open('250719_163931/commands.pkl', 'rb') as f:
    commands = pickle.load(f)

set_renderer(True)
apply_commands(state, commands, time_step=0.5, verbose=True)

from pybullet_planning.pybullet_tools.utils import wait_if_gui
wait_if_gui('Exit?')
reset_simulation()
disconnect()
