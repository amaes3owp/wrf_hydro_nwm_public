mpif90 -o Noah_wrfdriver_beta_mpp  ../IO_code/Noah_driver_wrfcode.o ../IO_code/module_Noahlsm_wrf_input_rt.o ../IO_code/module_Noah_distr_routing.o ../IO_code/module_Noah_channel_routing.o ../IO_code/module_Noah_chan_param_init_rt.o ../WRF_code/module_sf_noahlsm_rt.o ../Noah_code/module_model_constants_rt.o ../Noah_code/module_Noahlsm_utility_rt.o ../Noah_code/module_date_utilities_rt.o ../IO_code/module_Noah_gw_baseflow.o ../MPP/mpp_land.o ../MPP/CPL_WRF.o  ../IO_code/module_RTLAND.o -L/home/weiyu/netcdf/lib -lnetcdff -lnetcdf
