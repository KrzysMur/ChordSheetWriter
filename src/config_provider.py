import os
import configparser as cp
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(message)s",
    # filename="../console_output.log"
)

script_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
resources_dir = os.path.normpath(os.path.abspath(os.path.join(script_dir, '..', 'resources')))
config_file_path = os.path.normpath(os.path.join(resources_dir, 'config.ini'))
icons_dir = os.path.normpath(os.path.join(resources_dir, "icons"))

logging.debug(f"Config file path: {config_file_path}")


class ConfigProvider:
    def __init__(self):
        self.config = cp.ConfigParser()
        self.config.read(config_file_path)

    def get(self, section, key):
        return self.config[section][key]

    def get_page_width(self):
        return self.config["page"]["page_width"]

    def get_top_margin(self):
        return self.config["page"]["top_margin"]

    def get_left_margin(self):
        return self.config["page"]["left_margin"]

    def get_right_margin(self):
        return self.config["page"]["right_margin"]

    def get_bottom_margin(self):
        return self.config["page"]["bottom_margin"]

    def get_line_spacing(self):
        return self.config["page"]["line_spacing"]

    def get_bar_line_width(self):
        return self.config["page"]["bar_line_width"]

    def get_bar_line_width_coefficient(self):
        return self.config["page"]["bar_line_width_coefficient"]

    def get_toolbar_button_size(self):
        return int(self.config["gui"]["toolbar_button_size"])

    def get_main_window_width(self):
        return int(self.config["gui"]["main_window_width"])

    def get_main_window_height(self):
        return int(self.config["gui"]["main_window_height"])

    def get_toolbar_group_spacing(self):
        return int(self.config["gui"]["toolbar_group_spacing"])

    def get_save_window_width(self):
        return int(self.config["gui"]["save_window_width"])

    def get_save_window_height(self):
        return int(self.config["gui"]["save_window_height"])

    def get_logging_level(self):
        return int(self.config["dev"]["logging_level"])

    def get_delete_log_after_successful_pdf_generation(self):
        return self.config["dev"]["delete_log_after_successful_pdf_generation"]


config = ConfigProvider()
