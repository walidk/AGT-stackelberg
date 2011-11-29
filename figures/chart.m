close all; clc; clear all;
a1 = 2;
a2 = 4;
c1 = 5;
c2 = 4;

b1 = 10;
b2 = 3;

n_points = 100;

fn1 = latency(a1,b1,c1);
fn2 = latency(a2,b2,c2);

flows1 = [linspace(0,c1,n_points),linspace(c1,0,n_points)];
flows2 = [linspace(0,c2,n_points),linspace(c2,0,n_points)];

lats1 = []; lats2 = [];
mode = [zeros(1,n_points), ones(1,n_points)];
for i = 1:2*n_points
    lats1(i) = fn1(flows1(i),mode(i));
    lats2(i) = fn2(flows2(i),mode(i));
end

plot(flows1,lats1,'k-.','LineWidth',4)
hold on
plot(flows2,lats2,'k','LineWidth',4)
legend('Link 1','Link 2');
ylim([0,12]);
xlabel('Flow');
ylabel('Latency');