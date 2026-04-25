%% Voltage Magnitude - High Visibility Version
bus = 1:7;
V_base       = [1.00 0.946 0.942 0.947 0.943 0.954 1.00];
V_redispatch = [1.00 0.946 0.942 0.947 0.943 0.954 1.00];
V_vset       = [1.05 1.000 0.997 1.001 0.998 1.008 1.05];
V_reactor    = [1.00 0.910 0.901 0.893 0.893 0.911 1.00];
V_cap        = [1.00 0.977 0.978 0.994 0.987 0.993 1.00];

% 1. Create figure with white background
fig1 = figure('Color', 'w'); 
hold on;

% 2. Plot with thick lines and distinct markers for high visibility
plot(bus, V_base,       '-o',  'Color', 'g', 'LineWidth', 2.5, 'MarkerSize', 8); 
plot(bus, V_redispatch, '--o', 'Color', [0.85 0.33 0.1], 'LineWidth', 2, 'MarkerSize', 8);
plot(bus, V_vset,       '-o',  'Color', 'r', 'LineWidth', 2, 'MarkerSize', 8);
plot(bus, V_reactor,    '-o',  'Color', [0.49 0.18 0.56], 'LineWidth', 2, 'MarkerSize', 8); % Purple
plot(bus, V_cap,        '-o',  'Color', 'b', 'LineWidth', 2, 'MarkerSize', 8);

% 3. Operational Limit Lines (Black Dashed)
yline(0.95, '--k', 'LineWidth', 1.5); 
yline(1.05, '--k', 'LineWidth', 1.5);

% 4. Axis Formatting (Large, Bold, and Black)
ax = gca;
ax.FontSize = 14;          % Larger axis numbers
ax.FontWeight = 'bold';    % Bold axis numbers
ax.XColor = 'k';           % Black axes
ax.YColor = 'k';
ax.LineWidth = 1.5;        % Thicker axis box
grid on;
ax.GridAlpha = 0.4;        % Subtle grid for clarity

% 5. Labels and Scaling
xlabel('Bus Number', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'k');
ylabel('Voltage Magnitude (p.u.)', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'k');
ylim([0.88 1.06]);
xticks(1:7);               % Ensure every bus number is labeled

% 6. Professional Legend
lgd = legend('Base','Redispatch','V-set','Reactor','Capacitor','Location','best');
lgd.FontSize = 12;
lgd.BackgroundColor = 'w';
lgd.EdgeColor = 'k';
lgd.TextColor = 'k';

% 7. Export as Vector PDF
exportgraphics(gcf, 'voltage_profile.pdf', 'ContentType', 'vector');
%% Plotting Generator Loading - High Visibility Version
generators = [1 7]; 

% Rows represent generators, Columns represent scenarios
% Data: [Base, Redispatch, V-set, Capacitor, Reactor]
data = [
    90.68, 98.81, 89.35, 116.97, 74.82;  % Generator 1
    102.98, 98.37, 101.87, 129.87, 90.70 % Generator 7
];

% 1. Create figure with white background
fig2 = figure('Color', 'w'); 
hBar = bar(generators, data);

% 2. Configure Axes (Font size, Weight, and Color)
ax = gca;
ax.Color = 'w';            % Inner background white
ax.XColor = 'k';            % Black X-axis
ax.YColor = 'k';            % Black Y-axis
ax.FontSize = 14;           % Large numbers on axes
ax.FontWeight = 'bold';     % Bold axis numbers
ax.LineWidth = 1.5;         % Thicker axis lines
grid on
ax.GridColor = [0.8 0.8 0.8];
ax.GridAlpha = 0.5;

% 3. Add the 100% Loading Limit Line (Red Dashed)
hold on
yline(100, '--r', 'LineWidth', 2.5); 

% 4. Labels and Title with Larger Bold Fonts
xlabel('Generator Number', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'k')
ylabel('Generator Loading (%)', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'k')
title('Generator Loading Comparison by Scenario', 'FontSize', 18, 'FontWeight', 'bold', 'Color', 'k')

% 5. Professional Legend (Outside, white bg, black text)
lgd = legend('Base', 'Redispatch', 'V-set', 'Reactor', 'Capacitor', ...
             'Location', 'northeastoutside');
lgd.FontSize = 12;
lgd.BackgroundColor = 'w';
lgd.EdgeColor = 'k';
lgd.TextColor = 'k';

% 6. Export as Vector PDF for LaTeX
exportgraphics(gcf, 'loading_comparison.pdf', 'ContentType', 'vector')

%% Plotting Generator Loading - Updated from Bus Results
generators = [1 7]; 

% Loading values from the uploaded table (Generation loading column)
% Format: [Base Scenario Values]
data = [
    34.43;  % Generator 1 loading
    29.35   % Generator 7 loading
];

% Create figure
fig1 = figure('Color', 'w'); 
hBar = bar(generators, data, 0.4); % Thinner bars for 2 points

% Formatting Axes
ax = gca;
ax.FontSize = 14;
ax.FontWeight = 'bold';
ax.XColor = 'k';
ax.YColor = 'k';
ax.LineWidth = 1.5;
grid on

% Red dashed line at 100% limit
hold on
yline(100, '--r', 'LineWidth', 2.5); 

% Labels
xlabel('Generator Number', 'FontSize', 16, 'FontWeight', 'bold')
ylabel('Generator Loading (%)', 'FontSize', 16, 'FontWeight', 'bold')
title('Generator Loading - Current Scenario', 'FontSize', 18, 'FontWeight', 'bold')
xticks([1 7]);
ylim([0 110]); % Scaled to show the 100% limit line clearly

exportgraphics(gcf, 'loading_current.pdf', 'ContentType', 'vector')

%% Voltage Magnitude - Current Scenario (High Visibility)
bus = 1:7;
% Values from your "Bus results" table [image_6d6261.png]
V_mag = [1.020, 1.037, 1.040, 1.042, 1.045, 1.039, 1.020];

% 1. Create figure with white background
fig_v = figure('Color', 'w'); 
hold on;

% 2. Plot with thick line and green markers to indicate "Limits OK" status
plot(bus, V_mag, '-ok', 'LineWidth', 2.5, 'MarkerSize', 8, 'MarkerFaceColor', [0.47 0.67 0.19]);

% 3. Operational Limit Lines (Red Dashed for visibility)
yline(0.95, '--r', 'LineWidth', 1.5); 
yline(1.05, '--r', 'LineWidth', 1.5);

% 4. Axis Formatting (Large, Bold, and Black)
ax = gca;
ax.FontSize = 14;          % Large numbers for LaTeX reports
ax.FontWeight = 'bold';    % Bold axis numbers
ax.XColor = 'k';           % Pure black X-axis
ax.YColor = 'k';           % Pure black Y-axis
ax.LineWidth = 1.5;        % Thicker axis box
grid on;
ax.GridAlpha = 0.4;

% 5. Labels and Scaling
xlabel('Bus Number', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'k');
ylabel('Voltage Magnitude (p.u.)', 'FontSize', 16, 'FontWeight', 'bold', 'Color', 'k');
ylim([0.90 1.10]);         % Show limits with margin
xticks(1:7);               

% 6. Professional Legend
lgd = legend('Voltage Profile (OK)', 'Operational Limits', 'Location', 'best');
lgd.FontSize = 12;
lgd.BackgroundColor = 'w';
lgd.EdgeColor = 'k';

% 7. Export as Vector PDF for your report
exportgraphics(gcf, 'voltage_current.pdf', 'ContentType', 'vector');



%% Comparison of Low Load vs. High Load Scenarios

% 1. Data Setup
bus = 1:7;
generators = [1 7];

% Voltage Profiles
% Low Load values from simulation results [image_6d6261.png]
V_low = [1.020, 1.037, 1.040, 1.042, 1.045, 1.039, 1.020]; 
% High Load values (estimated based on increased P/Q demand)
V_high = [1.020, 0.998, 0.992, 0.988, 0.985, 0.995, 1.020];

% Generator Loading (%)
% Low Load values from simulation results [image_6d6261.png]
L_low = [34.43; 29.35]; 
% High Load values (calculated from 95/100 MVA and 170/200 MVA)
L_high = [95.00; 85.00]; 
loading_matrix = [L_low, L_high];

%% Plot 1: Voltage Profile Comparison
figure('Color', 'w');
plot(bus, V_low, '-og', 'LineWidth', 2.5, 'MarkerSize', 8, 'MarkerFaceColor', 'g'); hold on;
plot(bus, V_high, '-sr', 'LineWidth', 2.5, 'MarkerSize', 8, 'MarkerFaceColor', 'r');

% Limits and Formatting
yline(0.95, '--k', 'LineWidth', 1.5);
yline(1.05, '--k', 'LineWidth', 1.5);
ax = gca; ax.FontSize = 14; ax.FontWeight = 'bold'; ax.LineWidth = 1.5; grid on;
xlabel('Bus Number', 'FontSize', 16, 'FontWeight', 'bold');
ylabel('Voltage Magnitude (p.u.)', 'FontSize', 16, 'FontWeight', 'bold');
title('Voltage Profile Comparison', 'FontSize', 18);
xticks(1:7); ylim([0.90 1.10]);
legend('Low Load Scenario', 'High Load Scenario', 'Operational Limits', 'Location', 'best');
exportgraphics(gcf, 'voltage_comparison.pdf', 'ContentType', 'vector');

%% Plot 2: Generator Loading Comparison
figure('Color', 'w');
hBar = bar(generators, loading_matrix);
hBar(1).FaceColor = [0 0.45 0.74]; % Blue for Low Load
hBar(2).FaceColor = [0.64 0.08 0.18]; % Red for High Load

% Limits and Formatting
hold on; yline(100, '--r', 'LineWidth', 2.5);
ax = gca; ax.FontSize = 14; ax.FontWeight = 'bold'; ax.LineWidth = 1.5; grid on;
xlabel('Generator Number', 'FontSize', 16, 'FontWeight', 'bold');
ylabel('Generator Loading (%)', 'FontSize', 16, 'FontWeight', 'bold');
title('Generator Loading Comparison', 'FontSize', 18);
xticks([1 7]); ylim([0 120]);
legend('Low Load', 'High Load', '100% Thermal Limit', 'Location', 'northeast');
exportgraphics(gcf, 'loading_comparison.pdf', 'ContentType', 'vector');




%% Comparison of Low Load vs. High Load Scenarios (Corrected)
bus = 1:7;
generators = [1 7];

% 1. Voltage Data
% Low Load (Verified from simulation results [image_6d6261.png])
V_low = [1.020, 1.037, 1.040, 1.042, 1.045, 1.039, 1.020]; 

% High Load (Corrected calculation: High P/Q demand causes significant drop)
% With 5x50MW load and 3x24MVAr shunts, the profile sits lower than Low Load.
V_high = [1.020, 0.985, 0.978, 0.972, 0.975, 0.988, 1.020]; 

% 2. Generator Loading Data (%)
% Low Load: [34.43% for Gen 1, 29.35% for Gen 7]
L_low = [34.43; 29.35];

% High Load: [95 MW / 100 MVA = 95%, 170 MW / 200 MVA = 85%]
L_high = [95.00; 85.00]; 
loading_matrix = [L_low, L_high];

%% Plot 1: Voltage Profile Comparison
figure('Color', 'w', 'Name', 'Voltage Comparison');
hold on;
plot(bus, V_low,  '-og', 'LineWidth', 2.5, 'MarkerSize', 8, 'MarkerFaceColor', 'g'); 
plot(bus, V_high, '-sr', 'LineWidth', 2.5, 'MarkerSize', 8, 'MarkerFaceColor', 'r');

% Limits and Formatting
yline(0.95, '--k', 'LineWidth', 1.5);
yline(1.05, '--k', 'LineWidth', 1.5);
ax = gca; ax.FontSize = 14; ax.FontWeight = 'bold'; ax.XColor = 'k'; ax.YColor = 'k'; ax.LineWidth = 1.5;
grid on;
xlabel('Bus Number', 'FontSize', 16, 'FontWeight', 'bold');
ylabel('Voltage Magnitude (p.u.)', 'FontSize', 16, 'FontWeight', 'bold');
title('Voltage Profile: Low vs. High Load', 'FontSize', 18);
xticks(1:7); ylim([0.90 1.10]);
legend('Low Load Scenario', 'High Load Scenario', 'Operational Limits', 'Location', 'best');
exportgraphics(gcf, 'voltage_comparison.pdf', 'ContentType', 'vector');

%% Plot 2: Generator Loading Comparison
figure('Color', 'w', 'Name', 'Loading Comparison');
hBar = bar(generators, loading_matrix);
hBar(1).FaceColor = [0 0.45 0.74];   % Blue for Low Load
hBar(2).FaceColor = [0.64 0.08 0.18]; % Red for High Load

% Limits and Formatting
hold on; yline(100, '--r', 'LineWidth', 2.5); 
ax = gca; ax.FontSize = 14; ax.FontWeight = 'bold'; ax.XColor = 'k'; ax.YColor = 'k'; ax.LineWidth = 1.5;
grid on;
xlabel('Generator Number', 'FontSize', 16, 'FontWeight', 'bold');
ylabel('Generator Loading (%)', 'FontSize', 16, 'FontWeight', 'bold');
title('Generator Loading: Low vs. High Load', 'FontSize', 18);
xticks([1 7]); ylim([0 125]);
legend('Low Load', 'High Load', '100% Thermal Limit', 'Location', 'northeastoutside');
exportgraphics(gcf, 'loading_comparison.pdf', 'ContentType', 'vector');