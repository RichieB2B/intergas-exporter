# This is intergas-exporter

An Intergas boiler data exporter for prometheus

Inspired by the code samples posted on
https://www.circuitsonline.net/forum/view/80667
and
https://github.com/rickvanderzwet/IntergasBoilerReader

## Example output

![Image](examples/grafana-screenshot.png?raw=true)

> $ curl -s http://localhost:8080  
> &#35; HELP python_gc_objects_collected_total Objects collected during gc  
> &#35; TYPE python_gc_objects_collected_total counter  
> python_gc_objects_collected_total{generation="0"} 66.0  
> python_gc_objects_collected_total{generation="1"} 281.0  
> python_gc_objects_collected_total{generation="2"} 0.0  
> &#35; HELP python_gc_objects_uncollectable_total Uncollectable object found during GC  
> &#35; TYPE python_gc_objects_uncollectable_total counter  
> python_gc_objects_uncollectable_total{generation="0"} 0.0  
> python_gc_objects_uncollectable_total{generation="1"} 0.0  
> python_gc_objects_uncollectable_total{generation="2"} 0.0  
> &#35; HELP python_gc_collections_total Number of times this generation was collected  
> &#35; TYPE python_gc_collections_total counter  
> python_gc_collections_total{generation="0"} 38.0  
> python_gc_collections_total{generation="1"} 3.0  
> python_gc_collections_total{generation="2"} 0.0  
> &#35; HELP python_info Python platform information  
> &#35; TYPE python_info gauge  
> python_info{implementation="CPython",major="3",minor="7",patchlevel="3",version="3.7.3"} 1.0  
> &#35; HELP process_virtual_memory_bytes Virtual memory size in bytes.  
> &#35; TYPE process_virtual_memory_bytes gauge  
> process_virtual_memory_bytes 4.2094592e+07  
> &#35; HELP process_resident_memory_bytes Resident memory size in bytes.  
> &#35; TYPE process_resident_memory_bytes gauge  
> process_resident_memory_bytes 1.46432e+07  
> &#35; HELP process_start_time_seconds Start time of the process since unix epoch in seconds.  
> &#35; TYPE process_start_time_seconds gauge  
> process_start_time_seconds 1.63770026191e+09  
> &#35; HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.  
> &#35; TYPE process_cpu_seconds_total counter  
> process_cpu_seconds_total 0.9  
> &#35; HELP process_open_fds Number of open file descriptors.  
> &#35; TYPE process_open_fds gauge  
> process_open_fds 6.0  
> &#35; HELP process_max_fds Maximum number of open file descriptors.  
> &#35; TYPE process_max_fds gauge  
> process_max_fds 1024.0  
> &#35; HELP intergas_temperature_celcius Temperature in celsius  
> &#35; TYPE intergas_temperature_celcius gauge  
> intergas_temperature_celcius{type="aanvoer"} 69.97  
> intergas_temperature_celcius{type="flow"} 47.59  
> intergas_temperature_celcius{type="retour"} 36.57  
> intergas_temperature_celcius{type="warmwater"} 26.67  
> intergas_temperature_celcius{type="set"} 50.0  
> &#35; HELP intergas_water_pressure_bar Water pressure in bar  
> &#35; TYPE intergas_water_pressure_bar gauge  
> intergas_water_pressure_bar 1.7  
> &#35; HELP intergas_display_code Display code  
> &#35; TYPE intergas_display_code gauge  
> intergas_display_code 0.0  
> &#35; HELP intergas_fanspeed_rpm Fan speed in rpm  
> &#35; TYPE intergas_fanspeed_rpm gauge  
> intergas_fanspeed_rpm{type="set"} 1340.0  
> intergas_fanspeed_rpm{type="measured"} 1340.0  
> &#35; HELP intergas_fan_pwm Fan PWM duty cycle percentage  
> &#35; TYPE intergas_fan_pwm gauge  
> intergas_fan_pwm 8.2  
> &#35; HELP intergas_pump_pwm Pump PWM duty cycle percentage  
> &#35; TYPE intergas_pump_pwm gauge  
> intergas_pump_pwm 15.0  
> &#35; HELP intergas_flag Boolean flags  
> &#35; TYPE intergas_flag gauge  
> intergas_flag{name="gp_switch"} 1.0  
> intergas_flag{name="tap_switch"} 0.0  
> intergas_flag{name="roomtherm"} 0.0  
> intergas_flag{name="pump"} 1.0  
> intergas_flag{name="dwk"} 1.0  
> intergas_flag{name="alarm_status"} 0.0  
> intergas_flag{name="ch_cascade_relay"} 0.0  
> intergas_flag{name="opentherm"} 0.0  
> intergas_flag{name="gasvalve"} 0.0  
> intergas_flag{name="spark"} 0.0  
> intergas_flag{name="io_signal"} 1.0  
> intergas_flag{name="ch_ot_disabled"} 0.0  
> intergas_flag{name="low_water_pressure"} 0.0  
> intergas_flag{name="pressure_sensor"} 1.0  
> intergas_flag{name="burner_block"} 0.0  
> intergas_flag{name="grad_flag"} 1.0  
> &#35; HELP intergas_ionization_current_microampere Ionization current in µA  
> &#35; TYPE intergas_ionization_current_microampere gauge  
> intergas_ionization_current_microampere 7.33  
> &#35; HELP intergas_interrupt_time Interupt time  
> &#35; TYPE intergas_interrupt_time gauge  
> intergas_interrupt_time 200.0  
> &#35; HELP intergas_load Load %  
> &#35; TYPE intergas_load gauge  
> intergas_load{type="interrupt"} 135.84  
> intergas_load{type="main"} 25.125  
> &#35; HELP intergas_hours Duration in hours  
> &#35; TYPE intergas_hours gauge  
> intergas_hours{type="line_power"} 18491.0  
> intergas_hours{type="ch_function"} 3849.0  
> intergas_hours{type="dhw_function"} 246.0  
> &#35; HELP intergas_stats Statistics in number of times  
> &#35; TYPE intergas_stats gauge  
> intergas_stats{type="power_disconnect"} 1046.0  
> intergas_stats{type="burnerstarts"} 52436.0  
> intergas_stats{type="burnerstarts_dhw"} 14324.0  
> intergas_stats{type="ignition_failed"} 4.0  
> intergas_stats{type="flame_lost"} 1.0  
> intergas_stats{type="reset"} 3.0  
> &#35; HELP intergas_gasmeter Gas usage in m3  
> &#35; TYPE intergas_gasmeter gauge  
> intergas_gasmeter{type="cv"} 5383.3816  
> intergas_gasmeter{type="warmwater"} 519.1142  
> &#35; HELP intergas_watermeter Hot water usage in m3  
> &#35; TYPE intergas_watermeter gauge  
> intergas_watermeter 77.9017  
> &#35; HELP intergas_parameter Setting parameter  
> &#35; TYPE intergas_parameter gauge  
> intergas_parameter{type="heater_on"} 1.0  
> intergas_parameter{type="comfort_mode"} 0.0  
> intergas_parameter{type="ch_set_max"} 50.0  
> intergas_parameter{type="dhw_set"} 50.0  
> intergas_parameter{type="eco_days"} 3.0  
> intergas_parameter{type="comfort_set"} 0.0  
> intergas_parameter{type="dhw_at_night"} 0.0  
> intergas_parameter{type="ch_at_night"} 0.0  
> intergas_parameter{type="param_1"} 0.0  
> intergas_parameter{type="param_2"} 0.0  
> intergas_parameter{type="param_3"} 65.0  
> intergas_parameter{type="param_4"} 75.0  
> intergas_parameter{type="param_5"} 25.0  
> intergas_parameter{type="param_6"} -7.0  
> intergas_parameter{type="param_7"} 25.0  
> intergas_parameter{type="param_8"} 5.0  
> intergas_parameter{type="param_9"} 1.0  
> intergas_parameter{type="param_A"} 0.0  
> intergas_parameter{type="param_b"} 0.0  
> intergas_parameter{type="param_C"} 1.0  
> intergas_parameter{type="param_c"} 20.0  
> intergas_parameter{type="param_d"} 20.0  
> intergas_parameter{type="param_E"} 25.0  
> intergas_parameter{type="param_E."} 1.0  
> intergas_parameter{type="param_F"} 35.0  
> intergas_parameter{type="param_H"} 67.0  
> intergas_parameter{type="param_n"} 60.0  
> intergas_parameter{type="param_o"} 0.0  
> intergas_parameter{type="param_P"} 10.0  
> intergas_parameter{type="param_r"} 0.0  
> intergas_parameter{type="param_F."} 40.0  
> &#35; HELP intergas_tapflow Warm water tap flow  
> &#35; TYPE intergas_tapflow gauge  
> intergas_tapflow 0.0  
> &#35; HELP intergas_updated Intergas client last updated  
> &#35; TYPE intergas_updated gauge  
> intergas_updated 1.6377002632745795e+09  
> &#35; HELP intergas_up Intergas client status  
> &#35; TYPE intergas_up gauge  
> intergas_up 1.0  
