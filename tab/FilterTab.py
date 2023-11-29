import panel as pn
import holoviews as hv
import matplotlib.pyplot as plt

from bokeh.models import GlyphRenderer, LinearAxis, LinearScale, Range1d

import pandas as pd
import numpy as np
import GLOBAL_VARS as gv

from model.filter import Filter, Butterwoth, route_filter_class
from controller.setActions import plot_secondary

hv.extension('bokeh')
pn.extension()


class FilterTab:
    def __init__(self):
        self.ad = None  # Analog or Digital
        self.filter_dict = None  # Dict Butter, Cheby, FIR, IIR... with its methods and widgets
        self.filter_list = None  # List Butter, Cheby, FIR, IIR...
        self.filter_obj = None
        self.method_list = [None]
        self.window_dig_list = list(gv.window_scipy_types_dict.keys())
        self.plot_pane = pn.pane.HoloViews()

        from matplotlib.figure import Figure
        pn.extension()

        fig1 = Figure()
        ax1 = fig1.subplots()
        ax1.plot([1, 2, 3], [1, 2, 3])
        self.plot_polar = pn.pane.Matplotlib(fig1, dpi=144)

        ad_list = list(gv.filter_options_dict.keys())
        frequency_units_list = list(gv.frequency_units_dict.keys())
        self.set_select_ad(ad_list[0])

        ####################
        # SELECTOR WIDGETS #
        ####################
        self.select_ad_widget = pn.widgets.Select(options=ad_list,
                                                  value=ad_list[0],
                                                  name='Type of signal',
                                                  width=180)
        self.select_ad_widget.param.watch(self.set_select_ad, "value")
        self.select_filter_widget = pn.widgets.Select(options=self.filter_list,
                                                      value=self.filter_list[0],
                                                      name='Type of filter',
                                                      width=180)
        self.select_filter_widget.param.watch(self.set_select_filter, "value")

        self.select_method_widget = pn.widgets.Select(options=self.method_list,
                                                      value=self.method_list[0],
                                                      name='Method',
                                                      visible=False,
                                                      width=180)
        self.select_window_widget = pn.widgets.Select(options=self.window_dig_list,
                                                      value=self.window_dig_list[0],
                                                      name='Window',
                                                      visible=False,
                                                      width=180)
        # self.select_filter_widget.param.watch(self.set_select_type, "value")

        self.select_cutoff_units_widget = pn.widgets.Select(options=frequency_units_list,
                                                            value=frequency_units_list[0],
                                                            visible=False,
                                                            align="end",
                                                            width=60)
        self.select_fs_units_widget = pn.widgets.Select(options=frequency_units_list,
                                                        value=frequency_units_list[0],
                                                        visible=False,
                                                        align="end",
                                                        width=60)
        self.normalize_radio_button_group = pn.widgets.RadioButtonGroup(options=gv.normalize_options,
                                                                        value=gv.normalize_options[0],
                                                                        name='Normalize',
                                                                        visible=False)
        self.radio_pass_zero_widget = pn.widgets.RadioButtonGroup(options=list(gv.yes_no_options.keys()),
                                                                  name='Pass Zero',
                                                                  visible=False)
        self.radio_scale_widget = pn.widgets.RadioButtonGroup(options=list(gv.yes_no_options.keys()),
                                                              name='Scale',
                                                              visible=False)
        self.radio_pass_zero_widget.value = list(gv.yes_no_options.keys())[0]
        self.radio_scale_widget.value = list(gv.yes_no_options.keys())[1]

        ####################
        #   TEXT WIDGETS   #
        ####################
        self.text_hint = pn.widgets.StaticText(name='Hint', value='')
        self.text_f0_gain_value = pn.widgets.StaticText(name='Gain f0', value='', visible=False)
        self.text_fc_gain_value = pn.widgets.StaticText(name='Gain fc', value='', visible=False)
        self.text_fc_phase_value = pn.widgets.StaticText(name='Phase fc', value='', visible=False)
        self.text_hint.value = "Select A/D and type of filter."
        self.text_cutoff_help = pn.widgets.StaticText(name='Note', value='Low pass: i.e. 1000 with Pass zero True \n' +
                                                                         'High pass: i.e. 1000 with Pass zero False \n' +
                                                                         'Pass band: i.e. 100, 150 \n' +
                                                                         'Multi Pass band: i.e. 100, 150, 200, 250 '
                                                      , visible=False)
        self.text_pass_zero = pn.widgets.StaticText(name='Pass Zero', value='', visible=False)
        self.text_scale = pn.widgets.StaticText(name='Scale', value='', visible=False)

        ####################
        #  INPUT WIDGETS   #
        ####################
        self.input_cutoff_widget = pn.widgets.FloatInput(name='Cutoff frequency',
                                                         value=1.0,
                                                         start=0.1,
                                                         visible=False,
                                                         width=100)
        # input_cutoff_dig_widget Allows a list of frequencies for digital filters (as scipy argument)
        self.input_cutoff_dig_widget = pn.widgets.TextInput(name='Cutoff frequency',
                                                            visible=False,
                                                            width=100)
        self.input_order_widget = pn.widgets.IntInput(name='Order',
                                                      value=1,
                                                      start=1,
                                                      visible=False,
                                                      width=100)
        self.input_ripple_widget = pn.widgets.FloatInput(name='Ripple [dB]',
                                                         value=0.5,
                                                         start=0,
                                                         visible=False,
                                                         width=100)
        self.input_width_widget = pn.widgets.FloatInput(name='Width [same units fs]',
                                                        value=1,
                                                        start=0,
                                                        visible=False,
                                                        width=100)
        self.input_fs_widget = pn.widgets.FloatInput(name='Sample rate [Hz]',
                                                     value=44000,
                                                     start=0,
                                                     visible=False,
                                                     width=100)
        self.input_width_widget.value = None

        # # Checkbox widgets
        # self.seed_checkbox = pn.widgets.Checkbox(name='As random seed', visible=False, align='end')

        ####################
        #  BUTTON WIDGETS  #
        ####################
        self.calculate_button = pn.widgets.Button(name="Calculate", button_type="primary", visible=False)
        self.calculate_button.on_click(self.calculate_filter)
        self.text_hint.value = ''

        # Vars
        self.plot_column = pn.Column(self.normalize_radio_button_group,
                                     self.plot_pane,
                                     self.text_f0_gain_value,
                                     self.text_fc_gain_value,
                                     self.text_fc_phase_value,
                                     visible=False,
                                     styles=dict(background='WhiteSmoke'), width=700)

        self.plot_polar_column = pn.Column(self.plot_polar,
                                           visible=False,
                                           styles=dict(background='WhiteSmoke'), width=700)

        # Dictionary with all the widgets to make them visible or not
        self.widget_dict = {
            "select_ad_widget": self.select_ad_widget,
            "select_filter_widget": self.select_filter_widget,
            "select_method_widget": self.select_method_widget,
            "select_cutoff_units_widget": self.select_cutoff_units_widget,
            "select_window_widget": self.select_window_widget,
            "select_fs_units_widget": self.select_fs_units_widget,
            "normalize_radio_button_group": self.normalize_radio_button_group,
            "radio_pass_zero_widget": self.radio_pass_zero_widget,
            "radio_scale_widget": self.radio_scale_widget,
            "text_hint": self.text_hint,
            "text_f0_gain_value": self.text_f0_gain_value,
            "text_fc_gain_value": self.text_fc_gain_value,
            "text_fc_phase_value": self.text_fc_phase_value,
            "text_pass_zero": self.text_pass_zero,
            "text_scale": self.text_scale,
            "text_cutoff_help": self.text_cutoff_help,
            "input_cutoff_widget": self.input_cutoff_widget,
            "input_cutoff_dig_widget": self.input_cutoff_dig_widget,
            "input_order_widget": self.input_order_widget,
            "input_ripple_widget": self.input_ripple_widget,
            "input_width_widget": self.input_width_widget,
            "input_fs_widget": self.input_fs_widget,
            "calculate_button": self.calculate_button,
            "plot_column": self.plot_column,
            "plot_polar_column": self.plot_polar_column
        }
        # Make them visible or not
        self.set_visible_widgets(self.select_filter_widget.value)

        ####################
        # CONTENT WIDGETS  #
        ####################
        self.content = pn.Column(pn.Row(
            pn.Column(self.select_ad_widget,
                      self.select_filter_widget,
                      self.select_method_widget,
                      self.select_window_widget,
                      pn.Row(self.input_cutoff_widget,
                             self.input_cutoff_dig_widget,
                             self.select_cutoff_units_widget),
                      self.text_cutoff_help,
                      self.input_order_widget,
                      self.text_pass_zero,
                      self.radio_pass_zero_widget,
                      self.text_scale,
                      self.radio_scale_widget,
                      self.input_ripple_widget,
                      pn.Row(self.input_fs_widget,
                             self.select_fs_units_widget),
                      self.calculate_button,
                      ),
            self.plot_column,
            self.plot_polar_column,
            width=2500),
            pn.Column(self.text_hint))

    def set_select_ad(self, event):
        """
        Selector of Analog or Digital, change the selector of filter list
        :param event: scroll selector event
        :return: None
        """
        if isinstance(event, str):
            self.ad = event
            self.filter_dict = gv.filter_options_dict[self.ad]
            self.filter_list = list(self.filter_dict.keys())
        else:
            self.ad = event.obj.value
            self.filter_dict = gv.filter_options_dict[self.ad]
            self.filter_list = list(self.filter_dict.keys())
            self.select_filter_widget.options = self.filter_list
            self.select_filter_widget.value = self.filter_list[0]

    def set_select_filter(self, event):
        """
        Activate widgets input for selected filter
        :param event: event
        :return: None
        """
        filter_name_str = event.obj.value
        self.set_visible_widgets(filter_name_str)

    def set_visible_widgets(self, filter_name_str):
        """
        Activate widgets
        :param filter_name_str: filter type
        :return: None
        """
        self.method_list = list(self.filter_dict[filter_name_str].keys())
        default_method = self.method_list[0]
        self.select_method_widget.options = self.method_list
        self.select_method_widget.value = default_method
        widget_list = self.filter_dict[filter_name_str][default_method]['widgets']

        visible_widget_set = set(widget_list) & set(self.widget_dict.keys())
        invisible_widget_set = set(self.widget_dict.keys()) - set(widget_list)

        # Set visible and invisible items
        for v_i in visible_widget_set:
            self.widget_dict[v_i].visible = True
        for n_i in invisible_widget_set:
            self.widget_dict[n_i].visible = False

    def get_vars_dict(self, type_str, cutoff):
        """
        Get vars dict to create objects
        :param type_str, str with type
        :param cutoff, list or float
        :return: dict
        """
        scale = gv.yes_no_options[self.radio_scale_widget.value]
        if isinstance(cutoff, list) and len(cutoff) > 1:
            pass_zero = None
        else:
            pass_zero = gv.yes_no_options[self.radio_pass_zero_widget.value]

        if not (self.input_fs_widget is None):
            fs_units = gv.frequency_units_dict[self.select_fs_units_widget.value]
            fs = fs_units * self.input_fs_widget.value

        object_vars_dict = {"type_str": type_str,
                            "cutoff": cutoff,
                            "order": self.input_order_widget.value,
                            "gain": 1,
                            "ripple": self.input_ripple_widget.value,
                            "width": self.input_width_widget.value,
                            "window": self.select_window_widget.value,
                            "pass_zero": pass_zero,
                            "scale": scale,
                            "fs": fs}
        return object_vars_dict

    def calculate_filter(self, event):
        """
        Calculate filter response and plot it.
        :param event: Button click event
        :return: None
        """
        if self.select_ad_widget.value == "Analog":
            self.plot_analog()
        else:
            self.plot_digital()

    def plot_analog(self):
        """
        Plot analog type filters
        :return: None
        """
        cutoff = self.input_cutoff_widget.value * \
                 gv.frequency_units_dict[self.select_cutoff_units_widget.value]
        type_str = self.select_filter_widget.value

        object_vars_dict = self.get_vars_dict(type_str, cutoff)

        self.filter_obj = route_filter_class(object_vars_dict)

        self.text_f0_gain_value.visible = True
        self.text_fc_gain_value.visible = True
        self.text_fc_phase_value.visible = True
        self.normalize_radio_button_group.visible = False

        freq_units = gv.frequency_units_dict[self.select_cutoff_units_widget.value]
        n_points = max(int(100 * freq_units), 1000)  # Ensure a min of points
        n_points = min(n_points, int(100 * 1e3))
        end_point = complex(0, cutoff * freq_units * 10)
        init_point = complex(0, 0.10)
        values_x = np.geomspace(init_point, end_point, n_points)

        if self.normalize_radio_button_group.value == "Yes":
            values_x = values_x / cutoff
            w_cutoff = 1j
        else:
            w_cutoff = 2 * np.pi * cutoff

        phase_response_0_dict = self.filter_obj.calc_gain_phase_response(np.array([0j]))
        phase_response_cutoff_dict = self.filter_obj.calc_gain_phase_response(np.array([w_cutoff]))
        phase_response_values_dict = self.filter_obj.calc_gain_phase_response(values_x)

        self.text_f0_gain_value.value = str(round(phase_response_0_dict['Gain'][0], 3))
        self.text_fc_gain_value.value = str(round(phase_response_cutoff_dict['Gain'][0], 3))
        self.text_fc_phase_value.value = str(round(phase_response_cutoff_dict['Phase'][0] * (180 / np.pi), 3))

        gain_values = phase_response_values_dict['Gain']
        phase_values = phase_response_values_dict['Phase'] * (180 / np.pi)  # In deg

        gain_curve = hv.Curve((values_x.imag, gain_values),
                              'f/fc',
                              'Gain',
                              label='Gain').opts(tools=['hover'], width=500, height=300, title='Bode Plot',
                                                 logx=True, show_grid=True)
        phase_curve = hv.Curve((values_x.imag, phase_values),
                               'f/fc',
                               'Phase [º]',
                               label='Phase').opts(tools=['hover'], width=500, height=300, logx=True,
                                                   show_grid=True)
        vertical_cutoff_line = hv.VLine(x=1, label='Cutoff freq', ).opts(line_dash='dashed', line_color='black')

        self.plot_pane.object = (gain_curve * phase_curve.opts(hooks=[plot_secondary]) * vertical_cutoff_line)

        self.plot_column.visible = True

        self.text_hint.value = "Done."

    def plot_digital(self):
        """
        Plot digital type filters
        :return: None
        """
        cutoff_list = eval("[" + self.input_cutoff_dig_widget.value + "]")

        cutoff = np.array(cutoff_list) * \
                 gv.frequency_units_dict[self.select_cutoff_units_widget.value]
        type_str = self.select_filter_widget.value + "_" + self.select_method_widget.value

        object_vars_dict = self.get_vars_dict(type_str, cutoff)
        if len(cutoff_list) == 1 and not object_vars_dict["pass_zero"] and not object_vars_dict["order"] % 2 == 0:
            self.text_hint.value = "Order must be even if filter is high pass (pass zero = No)"
        elif np.max(cutoff) > object_vars_dict["fs"] / 2:
            self.text_hint.value = "Cutoff frequency must be minor than fs/2"
        else:
            fs = object_vars_dict['fs']

            self.filter_obj = route_filter_class(object_vars_dict)

            self.text_f0_gain_value.visible = False
            self.text_fc_gain_value.visible = False
            self.text_fc_phase_value.visible = False
            self.normalize_radio_button_group.visible = False

            scale = gv.frequency_units_dict[self.select_cutoff_units_widget.value]

            # self.text_f0_gain_value.value = str(round(phase_response_0_dict['Gain'][0], 3))
            # self.text_fc_gain_value.value = str(round(phase_response_cutoff_dict['Gain'][0], 3))
            # self.text_fc_phase_value.value = str(round(phase_response_cutoff_dict['Phase'][0] * (180 / np.pi), 3))

            # GAIN PHASE PLOT

            gain_values = self.filter_obj.get_gain(log=False)
            phase_values = self.filter_obj.get_phase(deg=True)  # In deg

            # Log axis does not allow values < 0.01
            # w = self.filter_obj.get_angular_axis()
            f_axis = self.filter_obj.get_freq_axis()
            index_f = np.where(f_axis >= 0.01)[0]
            f_axis = f_axis[index_f]
            gain_values = gain_values[index_f]
            phase_values = phase_values[index_f]

            dpi = 100
            width_inches = 5
            height_inches = 3

            gain_curve = hv.Curve((f_axis, gain_values),
                                  'f',
                                  'Gain',
                                  label='Gain').opts(tools=['hover'],
                                                     width=int(width_inches * dpi),
                                                     height=int(height_inches * dpi),
                                                     title='Bode Plot',
                                                     logx=True, show_grid=True)
            phase_curve = hv.Curve((f_axis, phase_values),
                                   'f',
                                   'Phase [º]',
                                   label='Phase').opts(tools=['hover'],
                                                       width=int(width_inches * dpi),
                                                       height=int(height_inches * dpi),
                                                       logx=True,
                                                       show_grid=True)
            self.plot_pane.object = gain_curve * phase_curve.opts(hooks=[plot_secondary])

            for i, cutoff_i in enumerate(cutoff):
                vertical_cutoff_line = hv.VLine(x=cutoff_i, label='Cutoff freq').opts(line_dash='dashed',
                                                                                      line_color='black')
                self.plot_pane.object *= vertical_cutoff_line

            self.plot_column.visible = True

            # ZERO POLE PLOT
            import matplotlib

            # Configurar el backend de Matplotlib
            plt.switch_backend('agg')
            # Activar la extensión de Matplotlib en Panel
            pn.extension('matplotlib')

            zeros = self.filter_obj.get_zeros()
            poles = self.filter_obj.get_poles()

            fig0, ax0 = plt.subplots(subplot_kw={'projection': 'polar'},
                                     figsize=(width_inches, height_inches), dpi=dpi)

            if len(zeros) > 0:
                r_zeros = np.abs(zeros)
                theta_zeros = np.angle(zeros)
                strm = ax0.scatter(theta_zeros, r_zeros, marker='o', color='b')

            if len(poles) > 0:
                r_poles = np.abs(poles)
                theta_poles = np.angle(poles)
                strm = ax0.scatter(theta_poles, r_poles, marker='x', color='r')

            theta_unit = np.arange(0, 2 * np.pi, 0.1)
            r_unit = np.ones(len(theta_unit))
            strm = ax0.plot(theta_unit, r_unit)

            ax0.set_title('Zero-Pole Plot')

            # self.plot_polar = pn.pane.Matplotlib(fig1, dpi=144)
            self.plot_polar = pn.pane.Matplotlib(fig0)
            self.plot_polar.visible = True
            self.plot_polar_column[0] = self.plot_polar
            self.plot_polar_column.visible = True

            self.text_hint.value = zeros
