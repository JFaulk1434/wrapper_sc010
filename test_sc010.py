#!/usr/bin/env python3
"""Test script for SC010 controller functions"""

import logging
from SC010 import Controller, ConnectionConfig
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")


def test_controller_functions():
    """Test all controller functions"""

    # First, try to find the controller
    print_section("Finding Controller")
    controller_info = Controller.find_controller()
    if not controller_info:
        logger.error("No SC010 controller found on the network")
        return

    logger.info(f"Found controller at IP: {controller_info['ip']}")
    logger.info(f"Controller MAC: {controller_info['mac']}")

    # Create controller instance
    config = ConnectionConfig(
        ip=controller_info["ip"],
        timeout=2.0,
        max_retries=3,
        retry_delay=1.0,
        gather_info=True,
    )

    try:
        with Controller(ip=controller_info["ip"], config=config) as controller:
            # Test basic controller info
            print_section("Controller Information")
            info = controller.get_controller_info()
            for key, value in info.items():
                logger.info(f"{key}: {value}")

            # Test device list functions
            print_section("Device List Functions")
            device_list = controller.get_devicelist()
            logger.info("Device List:")
            for device in device_list:
                logger.info(f"  - {device}")

            # Test device name functions
            print_section("Device Name Functions")
            device_names = controller.get_device_name()
            logger.info("Device Names and Aliases:")
            for device in device_names:
                logger.info(f"  - {device['trueName']} -> {device['alias']}")

            # Test matrix functions
            print_section("Matrix Functions")
            matrix = controller.get_matrix()
            logger.info("Current Matrix Configuration:")
            for mapping in matrix:
                logger.info(f"  - {mapping['tx']} -> {mapping['rx']}")

            # Test video wall functions
            print_section("Video Wall Functions")
            vw_config = controller.get_vw()
            logger.info("Video Wall Configuration:")
            for vw in vw_config:
                logger.info(f"  - Name: {vw['name']}")
                logger.info(f"    Rows: {vw['rows']}")
                logger.info(f"    Columns: {vw['cols']}")
                logger.info(f"    Encoder: {vw['encoder']}")

            # Test IP settings
            print_section("IP Settings")
            ip_settings = controller.get_ipsettings()
            logger.info("LAN(AV) Settings:")
            for key, value in ip_settings.items():
                logger.info(f"  - {key}: {value}")

            # Test device info for first device
            if device_list:
                print_section("Device Info")
                first_device = device_list[0]
                device_info = controller.get_device_info(first_device)
                logger.info(f"Info for {first_device}:")
                for key, value in device_info.items():
                    logger.info(f"  - {key}: {value}")

            # Test device status for first device
            if device_list:
                print_section("Device Status")
                first_device = device_list[0]
                device_status = controller.get_device_status(first_device)
                logger.info(f"Status for {first_device}:")
                for key, value in device_status.items():
                    logger.info(f"  - {key}: {value}")

            # Test device JSON
            print_section("Device JSON")
            device_json = controller.get_device_json()
            logger.info("Device JSON:")
            for device in device_json:
                logger.info(f"  - {device['trueName']} ({device['deviceType']})")
                logger.info(f"    Online: {device['online']}")
                logger.info(f"    IP: {device['ip']}")

            # Test scene JSON
            print_section("Scene JSON")
            scene_json = controller.get_scene_json()
            logger.info("Scene Configuration:")
            for scene in scene_json:
                logger.info(f"  - Scene: {scene['name']}")
                logger.info(f"    Layout: {scene.get('layout', 'N/A')}")

    except Exception as e:
        logger.error(f"Error during testing: {e}")


if __name__ == "__main__":
    test_controller_functions()
