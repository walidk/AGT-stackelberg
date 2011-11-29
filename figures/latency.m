function out = latency(a,b,c)
out = @out_fn;

    function out_val = out_fn(flow,mode)
        if mode == 0
            out_val = a;
            return;
        end
        out_val = b*(1/flow - 1/c) + a;
    end
end

        