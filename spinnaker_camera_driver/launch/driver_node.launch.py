# -----------------------------------------------------------------------------
# Copyright 2022 Bernd Pfrommer <bernd.pfrommer@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

example_parameters = {
    'blackfly_s': {
        'debug': False,
        'compute_brightness': False,
        'adjust_timestamp': True,            # ignored while PTP is on
        'frame_id': 'camera_optical_frame',
        'dump_node_map': False,              # set True once to confirm the added node names below

        # ---- image format
        'pixel_format': 'Mono8',
        'image_width': 1440,
        'image_height': 1080,
        'binning_x': 1,
        'binning_y': 1,
        'reverse_x': True,                   # calibration was done with these; keep
        'reverse_y': True,

        # ---- ISP (entries must exist in your copy of blackfly_s.yaml; see note)
        'gamma_enable': False,
        'sharpening_enable': False,
        'balance_white_auto': 'Off',         # run 'Once' on a white wall first, then Off

        # ---- exposure / gain: STATIC-TEST STATE (Tests 1, 2, 5)
        'exposure_auto': 'Off',
        'exposure_time': 50000.0,            # base for Test 2; adjust so the sheet reads 120-180 DN
        'gain_auto': 'Off',
        'gain': 0.0,
        # ---- exposure / gain: DYNAMIC-TEST STATE (Tests 3, 4, 6) - swap in when you get there
        # 'exposure_auto': 'Continuous',
        # 'exposure_auto_upper_limit': 4000.0,     # Test 3 sets the final value
        # 'exposure_auto_lower_limit': 50.0,
        # 'gain_auto': 'Continuous',
        # 'gain_auto_upper_limit': 18.0,           # Test 2 sets the final value
        # 'ae_target_grey_auto': 'Off',
        # 'ae_target_grey': 35.0,                  # Test 4 sets the final value
        # 'ae_ev_compensation': 0.0,
        # ae_damping: leave at camera default until Test 4

        # ---- GigE (measured on the TL-SG105E shared with the LiDAR; keep)
        'device_link_throughput_limit': 80000000,
        'gev_scps_packet_size': 1400,
        'gev_ieee_1588': True,
        'gev_ieee_1588_mode': 'SlaveOnly',
        'use_ieee_1588': True,

        # ---- acquisition
        'frame_rate_auto': 'Off',
        'frame_rate': 20.0,
        'frame_rate_enable': True,
        'trigger_mode': 'Off',
        'buffer_queue_size': 10,

        # ---- chunks (keep)
        'chunk_mode_active': True,
        'chunk_selector_frame_id': 'FrameID',
        'chunk_enable_frame_id': True,
        'chunk_selector_exposure_time': 'ExposureTime',
        'chunk_enable_exposure_time': True,
        'chunk_selector_gain': 'Gain',
        'chunk_enable_gain': True,
        'chunk_selector_timestamp': 'Timestamp',
        'chunk_enable_timestamp': True,

        # ---- diagnostics: was 39/41 (a 40 Hz leftover); camera runs at 20 Hz
        'diagnostic_period': 1.0,
        'diagnostic_min_freq': 19.0,
        'diagnostic_max_freq': 21.0,
    },
    'blackfly': {
        'debug': False,
        'dump_node_map': False,
        'gain_auto': 'Continuous',
        'pixel_format': 'BayerRG8',
        'exposure_auto': 'Continuous',
        'frame_rate_auto': 'Off',
        'frame_rate': 40.0,
        'frame_rate_enable': True,
        'buffer_queue_size': 10,
        'trigger_mode': 'Off',
        # 'stream_buffer_handling_mode': 'NewestFirst',
        # 'multicast_monitor_mode': False
    },
    'chameleon': {
        'debug': False,
        'compute_brightness': False,
        'dump_node_map': False,
        # set parameters defined in chameleon.yaml
        'gain_auto': 'Continuous',
        'exposure_auto': 'Continuous',
        'offset_x': 0,
        'offset_y': 0,
        'image_width': 2048,
        'image_height': 1536,
        'pixel_format': 'RGB8',  # 'BayerRG8, 'RGB8' or 'Mono8'
        'frame_rate_continous': True,
        'frame_rate': 100.0,
        'trigger_mode': 'Off',
        'chunk_mode_active': True,
        'chunk_selector_frame_id': 'FrameID',
        'chunk_enable_frame_id': True,
        'chunk_selector_exposure_time': 'ExposureTime',
        'chunk_enable_exposure_time': True,
        'chunk_selector_gain': 'Gain',
        'chunk_enable_gain': True,
        'chunk_selector_timestamp': 'Timestamp',
        'chunk_enable_timestamp': True,
    },
    'grasshopper': {
        'debug': False,
        'compute_brightness': False,
        'dump_node_map': False,
        # set parameters defined in grasshopper.yaml
        'gain_auto': 'Continuous',
        'exposure_auto': 'Continuous',
        'frame_rate_auto': 'Off',
        'frame_rate': 100.0,
        'trigger_mode': 'Off',
        'chunk_mode_active': True,
        'chunk_selector_frame_id': 'FrameID',
        'chunk_enable_frame_id': True,
        'chunk_selector_exposure_time': 'ExposureTime',
        'chunk_enable_exposure_time': True,
        'chunk_selector_gain': 'Gain',
        'chunk_enable_gain': True,
        'chunk_selector_timestamp': 'Timestamp',
        'chunk_enable_timestamp': True,
    },
    'flir_ax5': {
        'debug': False,
        'compute_brightness': False,
        'adjust_timestamp': False,
        'dump_node_map': False,
        # --- Set parameters defined in flir_ax5.yaml
        'pixel_format': 'Mono8',
        'gev_scps_packet_size': 576,
        'image_width': 640,
        'image_height': 512,
        'offset_x': 0,
        'offset_y': 0,
        'sensor_gain_mode': 'HighGainMode',  # "HighGainMode" "LowGainMode"
        'nuc_mode': 'Automatic',  # "Automatic" "External" "Manual"
        'sensor_dde_mode': 'Automatic',  # "Automatic" "Manual"
        'sensor_video_standard': 'NTSC30HZ',  # "NTSC30HZ" "PAL25Hz" "NTSC60HZ" "PAL50HZ"
        # valid values: "PlateauHistogram" "OnceBright" "AutoBright" "Manual" "Linear"
        'image_adjust_method': 'PlateauHistogram',
        'video_orientation': 'Normal',  # "Normal" "Invert" "Revert" "InvertRevert"
    },
}


def launch_setup(context, *args, **kwargs):
    """Launch camera driver node."""
    parameter_file = LaunchConfig('parameter_file').perform(context)
    camera_type = LaunchConfig('camera_type').perform(context)
    if not parameter_file:
        parameter_file = PathJoinSubstitution(
            [FindPackageShare('spinnaker_camera_driver'), 'config', camera_type + '.yaml']
        )
    if camera_type not in example_parameters:
        raise Exception('no example parameters available for type ' + camera_type)
    # binning:=2 / 4 (default 1 = unchanged). Binning is locked while the camera streams, so it only takes
    # effect at driver start. Width / height follow the full 1440x1080 sensor area. binning_mode:=Sum (default,
    # brighter pixels) or Average (same brightness as full resolution).
    binning = int(LaunchConfig('binning').perform(context))
    binning_mode = LaunchConfig('binning_mode').perform(context)
    if binning_mode not in ('Sum', 'Average'):
        raise Exception('binning_mode must be Sum or Average, not ' + binning_mode)
    overrides = {}
    if binning != 1:
        base = example_parameters[camera_type]
        overrides = {
            'binning_horizontal_mode': binning_mode,
            'binning_vertical_mode': binning_mode,
            'binning_x': binning,
            'binning_y': binning,
            'image_width': base['image_width'] // binning,
            'image_height': base['image_height'] // binning,
        }

    node = Node(
        package='spinnaker_camera_driver',
        executable='camera_driver_node',
        output='screen',
        # prefix=['xterm -e gdb --args'],
        name=[LaunchConfig('camera_name')],
        parameters=[
            example_parameters[camera_type],
            overrides,
            {
                'ffmpeg_image_transport.encoding': 'hevc_nvenc',
                'parameter_file': parameter_file,
                'serial_number': [LaunchConfig('serial')],
            },
        ],
        remappings=[
            ('~/control', '/exposure_control/control'),
        ],
    )

    return [node]


def generate_launch_description():
    """Create composable node by calling opaque function."""
    return LaunchDescription(
        [
            LaunchArg(
                'camera_name',
                default_value=['flir_camera'],
                description='camera name (ros node name)',
            ),
            LaunchArg(
                'camera_type',
                default_value='blackfly_s',
                description='type of camera (blackfly_s, chameleon...)',
            ),
            LaunchArg(
                'serial',
                default_value="'26215439'",
                description='FLIR serial number of camera (in quotes!!)',
            ),
            LaunchArg(
                'binning',
                default_value='1',
                description='sensor binning 1 / 2 / 4; image size follows',
            ),
            LaunchArg(
                'binning_mode',
                default_value='Sum',
                description='binning mode when binning != 1: Sum or Average',
            ),
            LaunchArg(
                'parameter_file',
                default_value='',
                description='path to ros parameter definition file (override camera type)',
            ),
            OpaqueFunction(function=launch_setup),
        ]
    )
