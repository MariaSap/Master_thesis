%%%%%%%%%%%%%%%%%%%%%%%%%%%  statistics.m %%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                          Author Sapounaki, Maria                                                                           %
%                                                                                                                                                                                             %
%  This code was written as a part of the master's thesis implementation for the statistical analysis of the data                  %
%  obtained by python simulation.                                                                                                                                          %
%                                                                                                                                                                                             %
%  It navigates to the Experiments folders and subsequently to the subfolders whose name starts with "Conf",                  %
%  receives the files containing the data for the characteristics of stiffness ellipsoids per each arm configuration.               %
%                                                                                                                                                                                             %
%  It performs:                                                                                                                                                                         %
%                       a. Descriptive Statistics across the different forces & create respective plots                                              %
%                                         (mean, median, standard deviation)                                                                                            %
%                       b. Descriptive Statistics across the different arm configurations & create respective plots                           %
%                                         (mean, median, standard                                                                                                            %
%                                         deviation)                                                                                                                                     %
%                       c. Pearson's Correlation Coefficient between forces and each characteristics per arm configuration          %
%                                                                                                                                                                                              %
%                       d. Percentage Difference for the pair forces                                                                                                  %
%                                                                                                                                                                                              %
%  The generated plots and csv are moved to "Statistics" folder, a subfolder of "Experiments".                                             %
%                                                                                                                                                                                              %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fv
clc
clear all
close all

%% Navigating in the folders of Experiments to receive the Characteristic_*.csv
% Get a list of all the folders in the 'Experiments' folder
mainFolder = '/Users/msapounaki/Dropbox/Studies/Master/Tübingen/Thesis/Code/Experiments';         % or ..../Code/Experiments_100ms
folders  = dir(mainFolder);

folders = folders([folders.isdir]);  % Filter out non-folders

% Loop through each folder
for i = 1:length(folders)
    folderName = folders(i).name;
    % Check if the folder starts with 'Conf'
    if startsWith(folderName, 'Conf') && folders(i).isdir
        subFolderPath = fullfile(mainFolder, folderName);

        % Get a list of all files in the current subfolder
        files = dir(fullfile(subFolderPath, 'Charac*')); % List files starting with 'Charac'
        
        % Loop through each file
        for j = 1:length(files)
            filename = files(j).name;
            filePath = fullfile(subFolderPath, filename);
            
            % Load the file and save it in a variable
            data = readtable(filePath); % Load the file
            
            variableName = strcat('Char_',folderName(6:end));


            % Save the loaded data into a variable
            assignin('base', variableName, data);
        end
    end
end



%% Read the data from the correspoding csv file for each arm configuration
% Eating
Force_eating          = table2array(Char_eating(:,1));
Orientation_eating  = table2array(Char_eating(:,2));
Shape_eating         = table2array(Char_eating(:,3));
Area_eating            = table2array(Char_eating(:,4));
 
% Extend
Force_extend          = table2array(Char_extend(:,1));
Orientation_extend = table2array(Char_extend(:,2));
Shape_extend        = table2array(Char_extend(:,3));
Area_extend           = table2array(Char_extend(:,4));

% Initila
Force_initial           = table2array(Char_initial(:,1));
Orientation_initial   = table2array(Char_initial(:,2));
Shape_initial          = table2array(Char_initial(:,3));
Area_initial             = table2array(Char_initial(:,4));

% Literature
Force_liter              = table2array(Char_liter(:,1));
Orientation_liter      = table2array(Char_liter(:,2));
Shape_liter             = table2array(Char_liter(:,3));
Area_liter                = table2array(Char_liter(:,4));

Force = Force_eating;   % it is equal to Force_extend, Force_initial,  Force_liter
%% Descriptive Statistics across the different forces
% Mean
mean_orientation  = [mean(Orientation_eating), mean(Orientation_extend), mean(Orientation_eating), mean(Orientation_liter)];
mean_shape         = [mean(Shape_eating), mean(Shape_extend), mean(Shape_eating), mean(Shape_liter)];
mean_area            = [mean(Area_eating), mean(Area_extend), mean(Area_eating), mean(Area_liter)];

% Median
mad_orientation    = [mad(Orientation_eating), mad(Orientation_extend), mad(Orientation_eating), mad(Orientation_liter)];
mad_shape           = [mad(Shape_eating), mad(Shape_extend), mad(Shape_eating), mad(Shape_liter)];
mad_area              = [mad(Area_eating), mad(Area_extend), mad(Area_eating), mad(Area_liter)];

% Std dev.
std_orientation       = [std(Orientation_eating), std(Orientation_extend), std(Orientation_eating), std(Orientation_liter)];
std_shape              = [std(Shape_eating), std(Shape_extend), std(Shape_eating), std(Shape_liter)];
std_area                = [std(Area_eating), std(Area_extend), std(Area_eating), std(Area_liter)];


%% Plots
figEat = figure('Name','Eating posture','NumberTitle','off','Position',[0 0 1500 1500]);

subplot(3,1,1)
plot(Force,Orientation_eating,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Orientation [rad]', 'FontSize', 44)
title('Orientation vs Force', 'FontSize', 50)

subplot(3,1,2)
plot(Force,Shape_eating,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Shape', 'FontSize', 44)
title('Shape vs Force', 'FontSize', 50)

subplot(3,1,3)
plot(Force,Area_eating,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Area [m^2]', 'FontSize', 44)
title('Area vs Force', 'FontSize', 50)


figExtend = figure('Name','Extended position','NumberTitle','off','Position',[0 0 1500 1500]);
subplot(3,1,1)
plot(Force,Orientation_extend,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Orientation [rad]', 'FontSize', 44)
title('Orientation vs Force', 'FontSize', 50)

subplot(3,1,2)
plot(Force,Shape_extend,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Shape', 'FontSize', 44)
title('Shape vs Force', 'FontSize', 50)

subplot(3,1,3)
plot(Force,Area_extend,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Area [m^2]', 'FontSize', 44)
title('Area vs Force', 'FontSize', 50)


figInitial = figure('Name','Initial position','NumberTitle','off','Position',[0 0 1500 1500]);
subplot(3,1,1)
plot(Force,Orientation_initial,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Orientation [rad]', 'FontSize', 44)
title('Orientation vs Force', 'FontSize', 50)

subplot(3,1,2)
plot(Force,Shape_initial,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Shape', 'FontSize', 44)
title('Shape vs Force', 'FontSize', 50)

subplot(3,1,3)
plot(Force,Area_initial,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Area [m^2]', 'FontSize', 44)
title('Area vs Force', 'FontSize', 50)


figLiter = figure('Name','Literature Position','NumberTitle','off','Position',[0 0 1500 1500]);
subplot(3,1,1)
plot(Force,Orientation_liter,'-o','LineWidth', 3);

ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Orientation [rad]', 'FontSize', 44)
title('Orientation vs Force', 'FontSize', 50)

subplot(3,1,2)
plot(Force,Shape_liter,'-o','LineWidth', 3);
ax = gca;
ax.XAxis.FontSize = 36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Shape', 'FontSize', 44)
title('Shape vs Force', 'FontSize', 50)

subplot(3,1,3)
plot(Force,Area_liter,'-o','LineWidth', 3);
ax=gca;
ax.XAxis.FontSize=36;
ax.YAxis.FontSize = 36;
xlabel('Applied force [N]', 'FontSize', 44)
ylabel('Area [m^2]', 'FontSize', 44)
title('Area vs Force', 'FontSize', 50)


saveas(figEat,'figEat.png')
saveas(figExtend,'figExtend.png')
saveas(figInitial,'figInitial.png')
saveas(figLiter,'figLiter.png')


%% Descriptive Statistics across the different arm configurations
for i=1:length(table2array(Char_eating))

    % Mean
       Orientation_mean(i) = mean([Orientation_eating(i),Orientation_extend(i),Orientation_initial(i),Orientation_liter(i)]);
       Shape_mean(i)        = mean([Shape_eating(i),Shape_extend(i),Shape_initial(i),Shape_liter(i)]);
       Area_mean(i)           = mean([Area_eating(i),Area_extend(i),Area_initial(i),Area_liter(i)]);

       % Median
       Orientation_mad(i) = mad([Orientation_eating(i),Orientation_extend(i),Orientation_initial(i),Orientation_liter(i)]);
       Shape_mad(i)        = mad([Shape_eating(i),Shape_extend(i),Shape_initial(i),Shape_liter(i)]);
       Area_mad(i)           = mad([Area_eating(i),Area_extend(i),Area_initial(i),Area_liter(i)]);

       % Standard Dev
       Orientation_std(i)   = std([Orientation_eating(i),Orientation_extend(i),Orientation_initial(i),Orientation_liter(i)]);
       Shape_std(i)          = std([Shape_eating(i),Shape_extend(i),Shape_initial(i),Shape_liter(i)]);
       Area_std(i)             = std([Area_eating(i),Area_extend(i),Area_initial(i),Area_liter(i)]);

end

Orientation_descrip = round([Orientation_mean;Orientation_mad;Orientation_std],4);
Shape_descrip        = round([Shape_mean;Shape_mad;Shape_std],4);
Area_descrip           =  round([Area_mean;Area_mad;Area_std],4);
 
tableData = [round(Orientation_descrip',4), round(Shape_descrip',4), round(Area_descrip',4) ];
ColVars    = {'Mean','Median','Std. Dev','Mean1','Median1','Std. Dev1','Mean2','Median2','Std. Dev2'};
tableToShow = array2table(tableData,'VariableNames', ColVars);

writetable(tableToShow, 'DescriptiveStatistics.csv');



%% Pearson's Correlation Coefficient

% Initial
CC_OrientInitial  = corr(Force, Orientation_initial, 'Type', 'Pearson');
CC_ShapeInitial = corr(Force, Shape_initial, 'Type', 'Pearson');
CC_AreaInitial    = corr(Force, Area_initial, 'Type', 'Pearson');
PearInitial           = round([CC_OrientInitial;CC_ShapeInitial;CC_AreaInitial],4);

% Extend
CC_OrientExte   = corr(Force, Orientation_extend, 'Type', 'Pearson');
CC_ShapeExte  = corr(Force, Shape_extend, 'Type', 'Pearson');
CC_AreaExte     = corr(Force, Area_extend, 'Type', 'Pearson');
PearExte            = round([CC_OrientExte;CC_ShapeExte;CC_AreaExte],4);


% Eating
CC_OrientEat     = corr(Force, Orientation_eating, 'Type', 'Pearson');
CC_ShapeEat    = corr(Force, Shape_eating, 'Type', 'Pearson');
CC_AreaEat       = corr(Force, Area_eating, 'Type', 'Pearson');
PearEat              = round([CC_OrientEat;CC_ShapeEat;CC_AreaEat],4);

% Literature
CC_OrientLit      = corr(Force, Orientation_liter, 'Type', 'Pearson');
CC_ShapeLit     = corr(Force, Shape_liter, 'Type', 'Pearson');
CC_AreaLit        = corr(Force, Area_liter, 'Type', 'Pearson');
PearLit               = round([CC_OrientLit;CC_ShapeLit; CC_AreaLit],4);


ColVars       = {'Initial','Extended','Eat','Literature'};
PearsonTbl = array2table([round(PearInitial,4) round(PearExte,4) round(PearEat,4) round(PearLit,4) ],  'VariableNames', ColVars);
writetable(PearsonTbl, 'PearsonTbl.csv');


%% Percentage Difference
col_cnt=1;
for i=1:length(Force)/2

       % Initial
           InitialPerDif(:,col_cnt) = [(abs(Orientation_initial(i) - Orientation_initial(i+9) ) / ((Orientation_initial(i) + Orientation_initial(i+9) ) / 2)) * 100; ...
                                                  (abs(Shape_initial(i) - Shape_initial(i+9) ) / ((Shape_initial(i) + Shape_initial(i+9) ) / 2)) * 100; ...  
                                                  (abs(Area_initial(i) - Area_initial(i+9) ) / ((Area_initial(i) + Area_initial(i+9) ) / 2)) * 100];

       % Extend
            ExtendPerDif(:,col_cnt) = [(abs(Orientation_extend(i) - Orientation_extend(i+9) ) / ((Orientation_extend(i) + Orientation_extend(i+9) ) / 2)) * 100; ...
                                                      (abs(Shape_extend(i) - Shape_extend(i+9) ) / ((Shape_extend(i) + Shape_extend(i+9) ) / 2)) * 100; ...  
                                                      (abs(Area_extend(i) - Area_extend(i+9) ) / ((Area_extend(i) + Area_extend(i+9) ) / 2)) * 100];

       % Eating
           EatingPerDif(:,col_cnt)= [(abs(Orientation_eating(i) - Orientation_eating(i+9) ) / ((Orientation_eating(i) + Orientation_eating(i+9) ) / 2)) * 100; ...
                                                   (abs(Shape_eating(i) - Shape_eating(i+9) ) / ((Shape_eating(i) + Shape_eating(i+9) ) / 2)) * 100; ...  
                                                   (abs(Area_eating(i) - Area_eating(i+9) ) / ((Area_eating(i) + Area_eating(i+9) ) / 2)) * 100];

       % Literaturex
         LiterPerDif (:,col_cnt)= [(abs(Orientation_liter(i) - Orientation_liter(i+9) ) / ((Orientation_liter(i) + Orientation_liter(i+9) ) / 2)) * 100; ...
                                               (abs(Shape_liter(i) - Shape_liter(i+9) ) / ((Shape_liter(i) + Shape_liter(i+9) ) / 2)) * 100; ...  
                                               (abs(Area_liter(i) - Area_liter(i+9) ) / ((Area_liter(i) + Area_liter(i+9) ) / 2)) * 100];

       col_cnt=col_cnt+1;
end


PercenCols       = {'0.5 vs 5','0.75 vs 7.5' , '1 vs 10', '1.25 vs 12.5', '1.5 vs 15','1.75 vs 17.5', '2 vs 20','2.5 vs 25','3 vs 30'};
PercentageDiff = array2table([round(InitialPerDif,4); round(ExtendPerDif,4); round(EatingPerDif,4); round(LiterPerDif,4) ],  'VariableNames', PercenCols);
writetable(PercentageDiff, 'PercentageDiff.csv');


%% Create folder for figures of statistics

newFoldName = strcat(mainFolder,'/Statistics');
mkdir(newFoldName)

movefile('*.csv',newFoldName)
movefile('*.png',newFoldName)


    
