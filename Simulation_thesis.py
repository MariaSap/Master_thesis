import csv
import math
import os
import mujoco as mj
import numpy as np
from OpenGL.GL import *
from mujoco.glfw import glfw
import glad

xml_path = 'bm_model.xml'  # xml file (assumes this is in the same folder as this file)
simend = 35000  # simulation time
print_camera_config = 1  # set to 1 to print camera config - this is useful for initializing view of the model)
loop_index=0 # For printing csv files

# For callback functions
button_left = False
button_middle = False
button_right = False
lastx = 0
lasty = 0

_overlay = {}


def add_overlay(gridpos,text1,text2):

    if gridpos not in _overlay:
        _overlay[gridpos] = ["",""]

    _overlay[gridpos][0] += text1 + "\n"
    _overlay[gridpos][1] += text2 + "\n"

def create_overlay(model,data):
    topleft = mj.mjtGridPos.mjGRID_TOPLEFT
    topright = mj.mjtGridPos.mjGRID_TOPRIGHT
    bottomleft = mj.mjtGridPos.mjGRID_BOTTOMLEFT
    bottomright = mj.mjtGridPos.mjGRID_BOTTOMRIGHT

    add_overlay(
        bottomleft,
        "Restart",'R',
    )
    add_overlay(
        bottomleft,
        "Normal",'N',
    )

    add_overlay(
        bottomleft,
        "Initial Position",'I',
    )

    add_overlay(
        bottomleft,
        "Distortion",'D',
    )

    add_overlay(
        bottomleft,
        "Time",'%.2f' %data.time,

    )

def init_save_data(fname,h0,h1,h2,h3,h4,h5,p,th,force, force_x, force_y):
    global loop_index
    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([h0,h1,h2,h3,h4,h5,p,th,force,force_x,force_y])

def save_data(model,data,fname,h1,h2,h3,h4,h5,p,th,force,force_x,force_y):
    global loop_index
    with open(fname, 'a', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(["Act_13", "Act_14", "Act_15"])
        writer.writerow([loop_index,h1,h2,h3,h4,h5,p,th,force,force_x,force_y])


def init_controller(model,data):
    p=0
    data.ctrl[:] = np.array([0.075, 0.015, 0.045, 0.000, 0.100, 0.180, 0.120, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.210, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.180, 0.300, 0.155, 0.000, 0.980])
    data.xfrc_applied[:] = np.zeros([17,6])
    mj.mj_step(model, data)
    return p


def controller(model,data,initial_activations,final_activations):
    #put the controller here. This function is controlled inside the simulation.
    global runtime, start_time,k
    if runtime - start_time <= hold_duration:

        # Set the muscle activations in the simulation
        data.ctrl[:] = final_activations + (initial_activations - final_activations) * dt
        print('G2F')
        activation_color()
        runtime = data.time

    else:
        print('G2I')
        data.ctrl[:] = initial_activations + (final_activations - initial_activations) * dt
        runtime = data.time
        activation_color()
        if runtime >= 2 * hold_duration * k:
            k = k + 1
            start_time = data.time
            # print(runtime)

    mj.mj_step(model, data)

def controller_noise(model, data, initial_activations, final_activations):
    # put the controller here. This function is controlled inside the simulation.
    global runtime, start_time, k, n, theta_degrees, p, flag, force_x, force_y, flag1, elv_angle, shoulder_elv, shoulder_rot, elbow_flex, pro_sup, elv_anglem, shoulder_elvm, shoulder_rotm, elbow_flexm, pro_supm
    if runtime <= k*hold_duration-5.9:
        # Set the muscle activations in the simulation
        data.ctrl[:] = final_activations + (initial_activations - final_activations) * dt
        p = 1
        print('Distortion - G2F')
        activation_color()
        runtime = data.time
        # data.xfrc_applied[:] = np.zeros([17, 6])

        # Pierre's snippet
        elv_angle = data.sensor('elv_angle_sensor')
        elv_angle = int(elv_angle.data)
        shoulder_elv = data.sensor('shoulder_elv_sensor')
        shoulder_elv = int(shoulder_elv.data)
        shoulder_rot = data.sensor('shoulder_rot_sensor')
        shoulder_rot = int(shoulder_rot.data)
        elbow_flex = data.sensor('elbow_flexion_sensor')
        elbow_flex = int(elbow_flex.data)
        pro_sup = data.sensor('pro_sup_sensor')
        pro_sup = int(pro_sup.data)

        # Maria's trial
        elv_anglem    = detect_joint_limit_violation(model, data, 11)
        shoulder_elvm = detect_joint_limit_violation(model, data, 12)
        shoulder_rotm = detect_joint_limit_violation(model, data, 14)
        elbow_flexm   = detect_joint_limit_violation(model, data, 15)
        pro_supm      = detect_joint_limit_violation(model, data, 16)

        if runtime >= k*hold_duration-6:
            p = 2
            force_x, force_y,force_magnitude  = theta_angles(theta_degrees)
            geom = model.geom_rgba[6:9]
            geom[:,:3] = [0.9, 0.02, .93]

            # Pierre's snippet
            elv_angle = data.sensor('elv_angle_sensor')
            elv_angle = int(elv_angle.data)
            shoulder_elv = data.sensor('shoulder_elv_sensor')
            shoulder_elv = int(shoulder_elv.data)
            shoulder_rot = data.sensor('shoulder_rot_sensor')
            shoulder_rot = int(shoulder_rot.data)
            elbow_flex = data.sensor('elbow_flexion_sensor')
            elbow_flex = int(elbow_flex.data)
            pro_sup = data.sensor('pro_sup_sensor')
            pro_sup = int(pro_sup.data)


            # Maria's trial
            elv_anglem = detect_joint_limit_violation(model, data, 11)
            shoulder_elvm = detect_joint_limit_violation(model, data, 12)
            shoulder_rotm = detect_joint_limit_violation(model, data, 14)
            elbow_flexm = detect_joint_limit_violation(model, data, 15)
            pro_supm = detect_joint_limit_violation(model, data, 16)

            print("Force of " + str(force_magnitude) + "N applied at " + str(theta_degrees) + "deg")

    else:
        p=0
        data.xfrc_applied[:] = np.zeros([17, 6])
        force_x, force_y = 0, 0
        print('Distortion - G2I')
        geom = model.geom_rgba[6:9]
        geom[:,:3] = [0.18, 0.96, 0.24]
        data.ctrl[:] = initial_activations + (final_activations - initial_activations) * dt
        runtime = data.time
        activation_color()

        # Pierre's snippet
        elv_angle = data.sensor('elv_angle_sensor')
        elv_angle = int(elv_angle.data)
        shoulder_elv = data.sensor('shoulder_elv_sensor')
        shoulder_elv = int(shoulder_elv.data)
        shoulder_rot = data.sensor('shoulder_rot_sensor')
        shoulder_rot = int(shoulder_rot.data)
        elbow_flex = data.sensor('elbow_flexion_sensor')
        elbow_flex = int(elbow_flex.data)
        pro_sup = data.sensor('pro_sup_sensor')
        pro_sup = int(pro_sup.data)

        # Maria's trial
        elv_anglem = detect_joint_limit_violation(model, data, 11)
        shoulder_elvm = detect_joint_limit_violation(model, data, 12)
        shoulder_rotm = detect_joint_limit_violation(model, data, 14)
        elbow_flexm = detect_joint_limit_violation(model, data, 15)
        pro_supm = detect_joint_limit_violation(model, data, 16)


        if runtime >= hold_duration * k:
            theta_degrees = theta_degrees + 45
            k = k + 1
            start_time = data.time
            flag1 = True
            if theta_degrees > 360:
                flag=True
            # print(runtime)

    mj.mj_step(model, data)
    return p, elv_angle, shoulder_elv, shoulder_rot, elbow_flex, pro_sup, elv_anglem, shoulder_elvm, shoulder_rotm, elbow_flexm, pro_supm

def activation_color():
        for i in range(len(model.actuator_gear)):
            if data.act[i] > 0.001:
                geom = model.tendon_rgba[i]
                geom[:3] = [0.9, 0.43, .43]  # Reset color to default
            else:
                geom = model.tendon_rgba[i]
                geom[:3] = [0.15, 0.3, 0.93]  # Reset color to default

def theta_angles(theta_degrees):
    # Define the angle in degrees and the force magnitude
    global force_magnitude, force_x, force_y

    # force_magnitude = random.randint(2, 40)
    # Convert the angle from degrees to radians
    theta_radians = math.radians(theta_degrees)

    # Calculate the force components along the x and y axes
    force_x = force_magnitude * math.cos(theta_radians)
    force_y = force_magnitude * math.sin(theta_radians)
    force_z = 0.0  # Assuming forces only in the x-y plane
    # Apply the external force to the body
    external_force = np.array([force_x, force_y, force_z])

    data.xfrc_applied[11, :3] = external_force

    return force_x, force_y, force_magnitude

def detect_joint_limit_violation(model, data, joint_id):

    # joint_id = model.joint_name2id(joint_name)
    joint_qpos = data.qpos[joint_id]
    joint_limit_lower, joint_limit_upper = model.jnt_range[joint_id]

    # Check if joint position is outside the limits
    if joint_qpos < joint_limit_lower or joint_qpos > joint_limit_upper:
        return True
    else:
        return False

        # return joint_violation

def keyboard(window, key, scancode, act, mods):
    if act == glfw.PRESS and key == glfw.KEY_R:
        mj.mj_resetData(model, data)
        mj.mj_forward(model, data)
        data.time=0
    if (act == glfw.PRESS and key == glfw.KEY_I):
        print('User input: I')
    if (act == glfw.PRESS and key == glfw.KEY_D):
        print('User input: D')
    if (act == glfw.PRESS and key == glfw.KEY_N):
        print('User input: N')


def mouse_button(window, button, act, mods):
    # update button state
    global button_left
    global button_middle
    global button_right

    button_left = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
    button_middle = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
    button_right = (glfw.get_mouse_button(
        window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)

    # update mouse position
    glfw.get_cursor_pos(window)


def mouse_move(window, xpos, ypos):
    # compute mouse displacement, save
    global lastx
    global lasty
    global button_left
    global button_middle
    global button_right

    dx = xpos - lastx
    dy = ypos - lasty
    lastx = xpos
    lasty = ypos

    # no buttons down: nothing to do
    if (not button_left) and (not button_middle) and (not button_right):
        return

    # get current window size
    width, height = glfw.get_window_size(window)

    # get shift key state
    PRESS_LEFT_SHIFT = glfw.get_key(
        window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
    PRESS_RIGHT_SHIFT = glfw.get_key(
        window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    mod_shift = (PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT)

    # determine action based on mouse button
    if button_right:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_MOVE_H
        else:
            action = mj.mjtMouse.mjMOUSE_MOVE_V
    elif button_left:
        if mod_shift:
            action = mj.mjtMouse.mjMOUSE_ROTATE_H
        else:
            action = mj.mjtMouse.mjMOUSE_ROTATE_V
    else:
        action = mj.mjtMouse.mjMOUSE_ZOOM

    mj.mjv_moveCamera(model, action, dx / height,
                      dy / height, scene, cam)


def scroll(window, xoffset, yoffset):
    action = mj.mjtMouse.mjMOUSE_ZOOM
    mj.mjv_moveCamera(model, action, 0.0, -0.05 *
                      yoffset, scene, cam)


# get the full path
dirname  = os.path.dirname(__file__)
abspath  = os.path.join(dirname + "/" + xml_path)
xml_path = abspath

## MuJoCo data structures
model = mj.MjModel.from_xml_path(xml_path)  # MuJoCo model
# Decrease the timestep to make the simulation faster
# model.opt.timestep = 0.001  # Each simulation step represents 1 millisecond.

data  = mj.MjData(model)  # MuJoCo data
cam   = mj.MjvCamera()  # Abstract camera
opt   = mj.MjvOption()  # visualization options

# force_vec = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 5, 7.5, 10, 12.5, 15, 17.5, 20, 25, 30]
force_vec = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3]


for i_l in force_vec:
    data.time = 0
    theta_degrees = 0
    force_x=0
    force_y=0
    elv_angle=0; shoulder_elv=0; shoulder_rot=0; elbow_flex=0; pro_sup=0
    elv_anglem = 0; shoulder_elvm = 0; shoulder_rotm = 0; elbow_flexm = 0; pro_supm = 0
    force_magnitude = i_l
    # duration of each movement in seconds
    dt=0.001

    n=0 # State of simulation - Normal, Initial, Distortion
    hold_duration = 20
    k=1
    p=0        # Define the seconds of force application. while p=2: force is applied, p=1 movement is unperturbed

    flag = False # for reaching 360 degs
    flag1 = True

    # Init GLFW, create window, make OpenGL context current, request v-sync
    glfw.init()
    window = glfw.create_window(1200, 900, "Force of " +str(force_magnitude)+" N", None, None)
    glfw.make_context_current(window)
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.6, 0.7, 0.2, 1.0)
    glfw.swap_interval(1)




    # initialize visualization data structures
    mj.mjv_defaultCamera(cam)
    mj.mjv_defaultOption(opt)
    scene = mj.MjvScene(model, maxgeom=10000)
    context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

    # install GLFW mouse and keyboard callbacks
    glfw.set_key_callback(window, keyboard)
    glfw.set_cursor_pos_callback(window, mouse_move)
    glfw.set_mouse_button_callback(window, mouse_button)
    glfw.set_scroll_callback(window, scroll)

    # Example on how to set camera configuration
    cam.azimuth = 118.49787597656237
    cam.elevation = -35.370190429687554
    cam.distance = 2.370037961847153
    cam.lookat = np.array([-0.005029708039576232, -0.004553573389907613, 0.46329891356313313])
    #
    # cam.azimuth = -0.8655273437501311
    # cam.elevation = -87.85823974609374
    # cam.distance = 2.370037961847153
    # cam.lookat = np.array([-0.005029708039576232, -0.004553573389907613, 0.46329891356313313])


    init_save_data("xpos_"+ "{:05.2f}".format(force_magnitude) +".csv", "Time", "Hand_x", "Hand_y","Hand_z", "Index3_x", "Index3_y","Index3_z","Theta","Mag. Of Force", "Force x", "Force y")
    init_save_data("qpos_"+ "{:05.2f}".format(force_magnitude) +".csv","Time", "Elv_ang", "Shoulder_ang","Shoulder_rot", "Elbow_flex", "Pro_sup","State","Theta","Mag. Of Force", "Force x", "Force y")
    init_save_data("qvel_"+ "{:05.2f}".format(force_magnitude) +".csv","Time", "Humerus", "Hand","Index1", "Index2", "Index3","State","Theta","Mag. Of Force", "Force x", "Force y")
    init_save_data("sensors" +  "{:05.2f}".format(force_magnitude)  + ".csv","Time", "elv_angle", "shoulder_elv", "shoulder_rot", "elbow_flex", "pro_sup", "State","Theta","Mag. Of Force", "Force x", "Force y")
    init_save_data("sensorsMaria" + "{:05.2f}".format(force_magnitude) + ".csv","Time", "elv_angle", "shoulder_elv", "shoulder_rot", "elbow_flex", "pro_sup", "State", "Theta", "Mag. Of Force", "Force x", "Force y")



    initial_activations = np.array([0.075, 0.015, 0.045, 0.000, 0.100, 0.180, 0.120, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.210, 0.000,0.000, 0.000, 0.000, 0.000, 0.000, 0.180, 0.250, 0.150, 0.000, 0.980])
    # #                               DELF   DELM   DELR   SUPSP  INFSP  SUBSC   TMIN   TMAΧ  PECM1   PECM2  PECM3   LAT1   LAT2   LAT3   CORB  TLong   Tlat   Tmed    ANC  SUP   BICL  BICs   BRA     BRD     PT    PQ
    # ConfExtend:
    # final_activations   = np.array([0.940, 0.000, 0.890, 0.800, 0.800, 0.800, 0.800, 0.870, 0.900, 0.500, 0.900, 0.000, 0.000, 0.000, 0.610, 0.000, 0.450, 0.000, 0.350, 0.000, 0.000, 0.370, 0.190, 0.000, 0.000, 0.100])

    # CongInitial:
    # final_activations = np.array([0.075, 0.015, 0.045, 0.000, 0.100, 0.180, 0.120, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.210, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.180, 0.250, 0.150, 0.000, 0.980])

    # Cong0: final_activations   =  np.array([0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000])
    # #                                DELF   DELM   DELR   SUPSP  INFSP  SUBSC  TMIN   TMAΧ  PECM1  PECM2  PECM3   LAT1   LAT2   LAT3   CORB  TLong   Tlat   Tmed    ANC    SUP   BICL   BICs    BRA    BRD    PT     PQ
    # ConfEating
    # final_activations   =  np.array([0.200, 0.980, 0.375, 0.850, 0.895, 0.575, 0.115, 0.260, 0.315, 0.500, 0.015, 0.160, 0.085, 0.095, 0.265, 0.000, 0.050, 0.055, 0.000, 0.77, 0.200, 0.500, 0.100, 0.050, 0.975, 0.000])

    # ConfLiter                       DELF   DELM   DELR   SUPSP  INFSP  SUBSC  TMIN   TMAΧ  PECM1  PECM2  PECM3   LAT1   LAT2   LAT3   CORB  TLong   Tlat   Tmed    ANC    SUP   BICL   BICs    BRA    BRD    PT     PQ
    final_activations =  np.array([0.160, 0.215, 0.140, 0.690, 0.585, 0.685, 0.190, 0.155, 0.245, 0.120, 0.000, 0.000, 0.000, 0.000, 0.000, 0.140, 0.110, 0.000, 0.610, 0.000, 0.090, 0.040, 0.000, 0.160, 0.275, 0.120])


    # final_activations = np.array([0.160, 0.515, 0.100, 0.290, 0.785, 0.685, 0.190, 0.155, 0.245, 0.120, 0.000, 0.000, 0.000, 0.000, 0.000, 0.140, 0.110, 0.000, 0.420, 0.000, 0.090, 0.040, 0.000, 0.120, 0.190, 0.420])

    start_time = data.time
    runtime    = data.time
    p = 0
    counter=1
    while not glfw.window_should_close(window):
        time_prev = data.time

        while (data.time - time_prev < 1.0/120):

            if counter<250:
                # initialize the controller
                init_controller(model, data)
                counter=counter+1
                data.time = 0

            # if (glfw.get_key(window, glfw.KEY_N) == glfw.PRESS or n == 0):
            #     n = 0
            #     controller(model, data, initial_activations, final_activations)
            #
            # if (glfw.get_key(window, glfw.KEY_I) == glfw.PRESS or n==1):
            #     n=1
            #     init_controller(model, data)
            #
            # if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS or n==2):
            #     n=2
            else:
                p, elv_angle, shoulder_elv, shoulder_rot, elbow_flex, pro_sup, elv_anglem, shoulder_elvm, shoulder_rotm, elbow_flexm, pro_supm = controller_noise(model, data, initial_activations, final_activations)

                if flag==True:
                    break

        if flag==True:
            print("Simulation  with is terminated. 360 deg were tested with "+ str(force_magnitude) + "N")
            break
                # mj.mj_step(model, data)

        save_data(model, data, "xpos_" + "{:05.2f}".format(force_magnitude) + ".csv", data.xpos[12][0], data.xpos[12][1],data.xpos[16][0], data.xpos[16][1], data.xpos[16][2], p, theta_degrees, force_magnitude, force_x, force_y)
        save_data(model, data, "qpos_" + "{:05.2f}".format(force_magnitude)+ ".csv", data.qpos[11],    data.qpos[12],   data.qpos[14],    data.qpos[15],    data.qpos[16],    p, theta_degrees, force_magnitude, force_x, force_y)
        save_data(model, data, "qvel_" + "{:05.2f}".format(force_magnitude) + ".csv", data.qvel[8],     data.qvel[12],   data.qvel[14],    data.qvel[15],    data.qvel[16],    p, theta_degrees, force_magnitude, force_x, force_y)
        save_data(model, data, "sensors" + "{:05.2f}".format(force_magnitude) + ".csv", elv_angle, shoulder_elv, shoulder_rot, elbow_flex, pro_sup, p, theta_degrees, force_magnitude, force_x, force_y)
        save_data(model, data, "sensorsMaria" + "{:05.2f}".format(force_magnitude) + ".csv", elv_anglem, shoulder_elvm, shoulder_rotm, elbow_flexm, pro_supm, p, theta_degrees, force_magnitude, force_x, force_y)
        loop_index = data.time

        if (data.time >= simend):
            break

        # get framebuffer viewport
        viewport_width, viewport_height = glfw.get_framebuffer_size(
            window)
        viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

        #create overlay
        create_overlay(model,data)

        #print camera configuration (help to initialize the view)
        if (print_camera_config==1):
            print('cam.azimuth =',cam.azimuth,';','cam.elevation =',cam.elevation,';','cam.distance = ',cam.distance)
            print('cam.lookat =np.array([',cam.lookat[0],',',cam.lookat[1],',',cam.lookat[2],'])')

        # Update scene and render
        mj.mjv_updateScene(model, data, opt, None, cam,
                           mj.mjtCatBit.mjCAT_ALL.value, scene)
        mj.mjr_render(viewport, scene, context)

        # overlay items
        for gridpos, [t1, t2] in _overlay.items():

            mj.mjr_overlay(
                mj.mjtFontScale.mjFONTSCALE_150,
                gridpos,
                viewport,
                t1,
                t2,
                context)

        # clear overlay
        _overlay.clear()

        # process pending GUI events, call GLFW callbacks
        glfw.poll_events()

        # swap OpenGL buffers (blocking call due to v-sync)
        glfw.swap_buffers(window)


    glfw.terminate()