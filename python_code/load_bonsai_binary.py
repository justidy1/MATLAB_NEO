import spikeinterface.core as si
import spikeinterface.preprocessing as sp

from probeinterface import Probe,combine_probes#,generate_linear_probe
import pandas as pd
##############################
##############################
### Create a 5 shank probe ###
##############################
##############################

probe_sites = pd.read_csv(r"ProbeInfo\NRX_Buzsaki64_buz_lin_5X12_JDY_probeinterface.csv", header=0)

probe_5x12 = Probe(ndim=2,si_units='um',manufacturer='NeuroNexus',model_name='A5x12-16-Buz-Lin-5mm-100-200-160-177')

probe1 = Probe(ndim=2,si_units='um',manufacturer='NeuroNexus',model_name='A5x12-16-Buz-Lin-5mm-100-200-160-177')
probe1.set_contacts(positions=probe_sites[['X','Y']].to_numpy()[(probe_sites['K']==1)], shapes='square', shape_params={'width': 10})

probe2 = probe1.copy()
probe2.move([200,0])

probe3 = Probe(ndim=2,si_units='um',manufacturer='NeuroNexus',model_name='A5x12-16-Buz-Lin-5mm-100-200-160-177')
probe3.set_contacts(positions=probe_sites[['X','Y']].to_numpy()[(probe_sites['K']==3) | (probe_sites['K']==6)], shapes='circle', shape_params={'radius': 15})
probe3.create_auto_shape('tip')

probe4 = probe1.copy()
probe4.move([600,0])

probe5 = probe1.copy()
probe5.move([800,0])

probe1.create_auto_shape('tip')
probe2.create_auto_shape('tip')
probe4.create_auto_shape('tip')
probe5.create_auto_shape('tip')

probe_5x12 = combine_probes([probe1,probe2,probe3,probe4,probe5])
probe_5x12.set_contact_ids(probe_sites['PhysicalChannel'].to_numpy(int)-1)
probe_5x12.set_device_channel_indices(probe_sites['OEChannel'].to_numpy()-1)

##############################
##############################
### Define function to extract the data ###
##############################
##############################
def get_traces_from_file(binary_file,ds,channels,start_frame,stop_frame):
    recording = si.read_binary(binary_file,
                                sampling_frequency=30000,
                                num_channels=64,dtype='uint16',
                                gain_to_uV=0.195,offset_to_uV=-0.195*32767)

    recording.set_probe(probe_5x12, group_mode='by_shank',in_place=True)

    global_job_kwargs = dict(chunk_duration="10s",n_jobs=16)
    si.set_global_job_kwargs(**global_job_kwargs)


    recording = sp.scale_to_uV(recording)
    recording = sp.decimate(recording,ds)

    if channels == -1:
        traces = recording.get_traces(0,start_frame,stop_frame)
    else:
        traces = recording.get_traces(0,start_frame,stop_frame,channel_ids=channels)

    return traces

traces = get_traces_from_file(binary_file,int(ds),channels,int(start_frame),int(stop_frame))

