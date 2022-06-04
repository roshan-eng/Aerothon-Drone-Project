% Dynamic Thrust Calculation

v = linspace(2, 10, 30);
rpm = linspace(4500, 13500, 30);
[V_cord, RPM_cord] = meshgrid(v, rpm);
z = @(V, RPM) RPM.* (4.39 * (10^-8) * (9^3.5) * ((RPM.* (4.5 * 4.23 * 10^-4 )) - V) ./ 9.8 * (4.5^0.5));
mesh(v, rpm, z(V_cord, RPM_cord))
title("Dynamic Thrust")
xlabel("Velocity (in m/s)")
ylabel("RPM")

