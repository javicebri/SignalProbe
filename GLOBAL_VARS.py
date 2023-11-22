

tabs_options_list = ["Filter", "Choke"]

filter_options_dict = {
    "Analog": {"Butterworth": {"unique": {"widgets": ["select_ad_widget",
                                                      "select_filter_widget",
                                                      "cutoff_input_widget",
                                                      "select_cutoff_units_widget",
                                                      "order_input_widget",
                                                      "calculate_button"]}
                               },
               "Chebyshev": {"unique": {"widgets": ["select_ad_widget",
                                                    "select_filter_widget",
                                                    "cutoff_input_widget",
                                                    "select_cutoff_units_widget",
                                                    "order_input_widget",
                                                    "ripple_input_widget",
                                                    "calculate_button"]}
                             }
               },
    "Digital": {"FIR": {"Least-squares": {"widgets": ["select_ad_widget",
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

Chebyshev_options_list = ["Type I", "Type II"]

frequency_units_dict = {
    "Hz": 1,
    "KHz": 1e3,
    "MHz": 1e6
}

normalize_options = ["Yes", "No"]
