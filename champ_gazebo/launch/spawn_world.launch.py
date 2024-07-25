import os

import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess,
                            IncludeLaunchDescription)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    gui = LaunchConfiguration("gui")
    headless = LaunchConfiguration("headless")
    paused = LaunchConfiguration("paused")
    lite = LaunchConfiguration("lite")
    gazebo_world = LaunchConfiguration("world")
    gz_pkg_share = launch_ros.substitutions.FindPackageShare(package="champ_gazebo").find(
        "champ_gazebo"
    )

    declare_use_sim_time = DeclareLaunchArgument("use_sim_time", default_value="True")
    declare_gui = DeclareLaunchArgument("gui", default_value="True")
    declare_headless = DeclareLaunchArgument("headless", default_value="False")
    declare_paused = DeclareLaunchArgument("paused", default_value="False")
    declare_lite = DeclareLaunchArgument("lite", default_value="False")
    declare_gazebo_world = DeclareLaunchArgument(
        "world", default_value=os.path.join(gz_pkg_share, "worlds/default.world")
    )

    pkg_share = launch_ros.substitutions.FindPackageShare(package="champ_description").find("champ_description")
    
    gazebo_config = os.path.join(launch_ros.substitutions.FindPackageShare(
        package="champ_gazebo"
    ).find("champ_gazebo"), "config/gazebo.yaml")
    launch_dir = os.path.join(pkg_share, "launch")
    # Specify the actions
    start_gazebo_server_cmd = ExecuteProcess(
        cmd=[
            "gzserver",
            "-s",
            "libgazebo_ros_init.so",
            "-s",
            "libgazebo_ros_factory.so",
            gazebo_world,
            '--ros-args',
            '--params-file',
            gazebo_config
        ],
        cwd=[launch_dir],
        output="screen",
    )

    start_gazebo_client_cmd = ExecuteProcess(
        condition=IfCondition(PythonExpression([" not ", headless])),
        cmd=["gzclient"],
        cwd=[launch_dir],
        output="screen",
    )

    return LaunchDescription(
        [
            declare_use_sim_time,
            declare_gui,
            declare_headless,
            declare_paused,
            declare_lite,
            declare_gazebo_world,
            start_gazebo_server_cmd,
            start_gazebo_client_cmd
        ]
    )
