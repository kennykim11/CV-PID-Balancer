import webcam, servo, pid

gen_pid = pid.pid(1, 0.25, 0.15, 300, 300)
gen_pid.send(None)
for x_pos in webcam.gen_ball_x('Ball Balancer'):
    new_pos = gen_pid.send(x_pos)