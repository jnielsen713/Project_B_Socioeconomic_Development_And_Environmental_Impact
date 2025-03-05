# Project B: Visualizing Socioeconomic Development and Environmental Impact
Joshua Nielsen  
Prof. Mike Ryu  
CS-150 Community Action Computing  

![Screenshot of the visualizer in action](/assets/Sample_Screenshot.png)

## Thesis Statement
I want to create a helpful system of visuals to help users compare global data regarding Gross Domestic Product (GDP) and Municipal Waste to highlight their corrolations and provoke insightful thinking on how the situation can be improved.

## Context
I am doing my course project on recycling, so when I was considering potential topics for this project my mind went straight to waste, since it is adjacent. I wanted to compare it with a measure of material production, which I believe I have found in GDP. I am pleased with the datasets I obtained. They came from  the OECD (the Organization for Economic Cooperation and Development). This appliction is meant to allow users to look country-by-country, on a time scale of almost 50 years, to see how the production and waste corrolate. You can view either statistic on a choropleth map, or see them both at once in a line chart corresponding to a particular country. The titles on the page change to tell you exactly what you are looking at during any given time.

## What am I Visualizing?
I am visualizing 50 years of data from two datasets: Gross Domestic Product per capita (in dollars), and Municipal Waste per capita (in kilograms). There are several callback funcitons which use the .csv files, dropdown menu, and sliderbar as inputs to update both graphics in an intuitive manner.

## Data Visualization Strategies
The page has two visuals, but to avoid it being too overwhelming they each get their own row. There is a dropdown menu which is clearly labeled that determines the data shown on the choropleth. The choropleth changes color depending on whether you are looking at global GDP or Waste. The bottom line graph is also labeled clearly with the name of the country it is displaying data from. This is updated whenever you click a valid country on the choropleth map. The line graph may have 2 y-axis, but both start at 0, and are clearly labeled and color-coded to the corresponding line. The purpose of this graph isn't to check exact values either, just to communicate change over time, which it does effectively. There is also a gray dashed line drawn on the graph via callback function which updates when you move the slider bar. It lines up with the year you currently have selected, which makes checking the data points for the lines on that exact year much easier. The slider bar is placed in the middle of the page as it manipulates both charts. Lastly, there is a nice dark-mode theme which makes the graphics and text stand out while not blinding the user with light mode.
