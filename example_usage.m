ds = 10;

r=pyrunfile("python_code\load_bonsai_binary.py","traces", ...
    binary_file='example_sig.bin', ... %'path\to\file.bin', ...
    ds=ds, ... % downsampling factor
    channels=py.list([0,1]), ... % which channels to get, if you want all set channels = -1. NOTE, starts AT ZERO, ends at 64
    start_frame=0, ... % start frame, in terms of fs/ds sampling rate
    stop_frame=3000); % end frame, in terms of fs/ds sampling rate

r_use = double(r); % the actual data to use
ts = ((0:size(r_use,1)-1)/(30000/ds))';


figure()
plot(ts,r_use(:,1))
xlabel("Time (s)")
ylabel("Voltage (uV)")