# This is intergas-exporter

An Intergas boiler data exporter for prometheus

Uses the python evohomeclient from:  
https://pypi.org/project/evohomeclient/  
https://github.com/watchforstock/evohome-client

Inspired by the code samples posted on
https://www.circuitsonline.net/forum/view/80667

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
> python_gc_collections_total{generation="0"} 41.0  
> python_gc_collections_total{generation="1"} 3.0  
> python_gc_collections_total{generation="2"} 0.0  
> &#35; HELP python_info Python platform information  
> &#35; TYPE python_info gauge  
> python_info{implementation="CPython",major="3",minor="7",patchlevel="3",version="3.7.3"} 1.0  
> &#35; HELP process_virtual_memory_bytes Virtual memory size in bytes.  
> &#35; TYPE process_virtual_memory_bytes gauge  
> process_virtual_memory_bytes 4.2053632e+07  
> &#35; HELP process_resident_memory_bytes Resident memory size in bytes.  
> &#35; TYPE process_resident_memory_bytes gauge  
> process_resident_memory_bytes 1.4688256e+07  
> &#35; HELP process_start_time_seconds Start time of the process since unix epoch in seconds.  
> &#35; TYPE process_start_time_seconds gauge  
> process_start_time_seconds 1.60677395231e+09  
> &#35; HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.  
> &#35; TYPE process_cpu_seconds_total counter  
> process_cpu_seconds_total 7685.64  
> &#35; HELP process_open_fds Number of open file descriptors.  
> &#35; TYPE process_open_fds gauge  
> process_open_fds 6.0  
> &#35; HELP process_max_fds Maximum number of open file descriptors.  
> &#35; TYPE process_max_fds gauge  
> process_max_fds 1024.0  
> &#35; HELP intergas_temperature_celcius Temperature in celsius  
> &#35; TYPE intergas_temperature_celcius gauge  
> intergas_temperature_celcius{type="aanvoer"} 44.08  
> intergas_temperature_celcius{type="flow"} 43.3  
> intergas_temperature_celcius{type="retour"} 42.92  
> intergas_temperature_celcius{type="warmwater"} 32.7  
> intergas_temperature_celcius{type="set"} 60.0  
> &#35; HELP intergas_water_pressure_bar Water pressure in bar  
> &#35; TYPE intergas_water_pressure_bar gauge  
> intergas_water_pressure_bar 1.71  
> &#35; HELP intergas_display_code Display code  
> &#35; TYPE intergas_display_code gauge  
> intergas_display_code 0.0  
> &#35; HELP intergas_fanspeed_rpm Fan speed in rpm  
> &#35; TYPE intergas_fanspeed_rpm gauge  
> intergas_fanspeed_rpm{type="set"} 0.0  
> intergas_fanspeed_rpm{type="measured"} 0.0  
> &#35; HELP intergas_fan_pwm Fan PWM duty cycle percentage  
> &#35; TYPE intergas_fan_pwm gauge  
> intergas_fan_pwm 0.0  
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
> intergas_flag{name="pressure_sensor"} 0.0  
> intergas_flag{name="burner_block"} 0.0  
> intergas_flag{name="grad_flag"} 0.0  
> &#35; HELP intergas_ionization_current_microampere Ionization current in µA  
> &#35; TYPE intergas_ionization_current_microampere gauge  
> intergas_ionization_current_microampere 0.0  
> &#35; HELP intergas_updated Intergas client last updated  
> &#35; TYPE intergas_updated gauge  
> intergas_updated 1.609160872862161e+09  
> &#35; HELP intergas_up Intergas client status  
> &#35; TYPE intergas_up gauge  
> intergas_up 1.0  
