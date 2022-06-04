% Endurance Estimation

Power = 403;
p = 1.02;
i_0 = 30;
v_0 = 4.23;
v_s = 3.7;
C_0 = 8 * 3600;
lmd = 0.8;

k = (v_0 - v_s) / (lmd * C_0);
t_0 = 30 * 60;
dt = 10;

i = [i_0 0];
v = [v_0 0];
c = [C_0 0];

n_iter = 100;
iter = [1, 2];
for j = 1:1:n_iter

    v(j + 1) = v(1) - k * (c(1) - c(j));
    i(j + 1) = Power / v(j + 1);

    syms n
    c(j + 1) = (i(j + 1) ^ (1 - p)) * (t_0 ^ (1 - p)) * (C_0 ^ p) - (sum(i(1 : j + 1)) * dt);

    iter(j + 1) = j;

%     if c(j + 1) <= (1 - lmd) * c(1)
%         break
%     end

end

plot(iter, c)