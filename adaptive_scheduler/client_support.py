import zmq

from adaptive_scheduler.slurm import get_job_id

ctx = zmq.Context()


def get_learner(url, learners, fnames):
    with ctx.socket(zmq.REQ) as socket:
        socket.connect(url)
        job_id = get_job_id()
        socket.send_pyobj(("start", job_id))
        reply = socket.recv_pyobj()
        if reply is None:
            raise RuntimeError(f'No learners to be run for {job_id}.')
        elif isinstance(reply, Exception):
            raise reply
        else:
            fname = reply
    learner = next(lrn for lrn, fn in zip(learners, fnames) if fn == fname)
    return learner, fname


def tell_done(url, fname):
    with ctx.socket(zmq.REQ) as socket:
        socket.connect(url)
        socket.send_pyobj(("stop", fname))
        socket.recv_pyobj()  # Needed because of socket type
