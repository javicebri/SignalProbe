
dpi = 50
bode_width = 640
bode_height = 480
polar_width = 3
polar_height = 3.34

tabs_options_list = ["Filter", "Noise", "Choke"]

filter_options_dict = {
    "Analog": {"Butterworth": {"unique": {"widgets": ["select_ad_widget",
                                                      "select_filter_widget",
                                                      "input_cutoff_widget",
                                                      "select_cutoff_units_widget",
                                                      "input_order_widget",
                                                      "calculate_button",
                                                      "text_hint"]}
                               },
               "Chebyshev": {"unique": {"widgets": ["select_ad_widget",
                                                    "select_filter_widget",
                                                    "input_cutoff_widget",
                                                    "select_cutoff_units_widget",
                                                    "input_order_widget",
                                                    "input_ripple_widget",
                                                    "calculate_button",
                                                    "text_hint"]}
                             }
               },
    "Digital": {"FIR": {"Window method (cutoff)": {"widgets": ["select_ad_widget",
                                                               "select_filter_widget",
                                                               "select_method_widget",
                                                               "input_cutoff_dig_widget",
                                                               "select_cutoff_units_widget",
                                                               "select_fs_units_widget",
                                                               "input_order_widget",
                                                               "input_width_widget",
                                                               "select_window_widget",
                                                               "radio_pass_zero_widget",
                                                               "radio_scale_widget",
                                                               "input_fs_widget",
                                                               "calculate_button",
                                                               "text_pass_zero",
                                                               "text_scale",
                                                               "text_hint"]},
                        "Window method (gain)": {"widgets": ["select_ad_widget",
                                                             "select_filter_widget",
                                                             "select_method_widget"]},
                        "Minimum phase": {"widgets": ["select_ad_widget",
                                                      "select_filter_widget",
                                                      "select_method_widget"]},
                        "Remez": {"widgets": ["select_ad_widget",
                                              "select_filter_widget",
                                              "select_method_widget"]},
                        "Least-squares": {"widgets": ["select_ad_widget",
                                                      "select_filter_widget",
                                                      "select_method_widget"]}
                        },
                "IIR": {"Least-squares": {"widgets": ["select_ad_widget",
                                                      "select_filter_widget",
                                                      "select_method_widget"]},
                        "Minimum phase": {"widgets": ["select_ad_widget",
                                                      "select_filter_widget",
                                                      "select_method_widget"]},
                        "Window method (cutoff)": {"widgets": ["select_ad_widget",
                                                               "select_filter_widget",
                                                               "select_method_widget"]},
                        "Window method (gain)": {"widgets": ["select_ad_widget",
                                                             "select_filter_widget",
                                                             "select_method_widget"]},
                        "Remez": {"widgets": ["select_ad_widget",
                                              "select_filter_widget",
                                              "select_method_widget"]}
                        }
                }
}

# Value if need additional input (None if not)
window_scipy_types_dict = {
    "boxcar": None,
    "triang": None,
    "blackman": None,
    "hamming": None,
    "hann": None,
    "bartlett": None,
    "flattop": None,
    "parzen": None,
    "bohman": None,
    "blackmanharris": None,
    "nuttall": None,
    "barthann": None,
    "cosine": None,
    "exponential": None,
    "tukey": None,
    "taylor": None,
    "lanczos": None,
    "kaiser": ["beta"],
    "kaiser_bessel_derived": ["beta"],
    "gaussian": ["std"],
    "general_cosine": ["w_coeffs"],
    "general_gaussian": ["needs", "power", "width"],
    "general_hamming": ["w_coeffs"],
    "dpss": ["normalized_half-bandwidth"],
    "chebwin": ["att"]

}

Chebyshev_options_list = ["Type I", "Type II"]

frequency_units_dict = {
    "Hz": 1,
    "KHz": 1e3,
    "MHz": 1e6
}

normalize_options = ["Yes", "No"]
yes_no_options = {"Yes": True, "No": False}
