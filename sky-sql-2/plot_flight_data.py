from sys import prefix
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib as mpl
import seaborn as sns
import folium


def plot_percentage_of_delayed_flights_per_airline(delay_per_airline : dict):
    airlines = list(delay_per_airline.keys())
    delays = list(delay_per_airline.values())
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.bar(airlines,delays)
    ax.set_title("Delay per airline per flight")
    ax.set_xlabel("Airline")
    ax.set_ylabel("Percentage delayed flights")
    ax.set_ylim(0, max(delays) + 5)
    plt.xticks(rotation=45, ha='right',fontsize=10)
    plt.tight_layout()  # make sure they fit
    plt.show()
    return fig


def plot_percentage_of_delayed_flight_per_hour(hours,percentages : list):
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.bar(hours, percentages)
    ax.set_title("% of delay per hour per day")
    ax.set_xlabel("hours")
    ax.set_ylabel("Percentage delayed flights")
    ax.set_ylim(0, max(percentages) + 5)
    # plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()  # make sure they fit
    plt.show()
    return fig

def plot_heatmap_routes(heat_map):
    #   The following code is based upon the use of Seaborn heatmaps, see also the following
    #   excellent Video:
    #   https://www.youtube.com/watch?v=u7ESlujjoBc

    # set the canvas size, return the image to fig
    fig,axs = plt.subplots(figsize=(40, 40))

    # Create the heatmap
    ax=sns.heatmap(heat_map, cmap = 'Blues',  annot = True,
                   annot_kws= {'size' : 10}, cbar=False, linewidths=1, linecolor='white')

    # Set the label for X=axis and Y-axis and the ticklables
    ax.set_xlabel('Origin')
    ax.set_ylabel('Destination')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right', fontsize=30)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right', fontsize=30)

    # Add padding to the X-axis & Y-axis lables

    ax.set_xlabel('Origin', labelpad=10, rotation=0, ha='right', fontsize=80)
    ax.set_ylabel('Destination', labelpad=10, rotation=90, ha='right', fontsize=80)

    # Rotate x-axis and y-axis labels to be horizontal
    # ax.xaxis.set_label_coords((0, 100))
    plt.show()
    # fig.savefig("Heat map routes.png")
    return fig

def get_line_color(percentage:float,per20, per50, per90) -> str:

    if percentage < per20:
        return "blue"
    elif percentage < per50:
        return "yellow"
    elif percentage < per90:
        return "orange"
    else:
        return "red"

def plot_map_with_routes(data):
    #   The following code is based upon the use of folium library, see also the following
    #   excellent Video:
    #   https://www.youtube.com/watch?v=j8tGVhaciNo

    # Initialize the roadmap from it's starting point, ie. BOSTON,
    # together with the zoom level. Adjust
    # this level to show the whole US.
    # Store this as m, which will be our map visualization.
    m = folium.Map(location=[44.58, -103.46], zoom_start=4) # Starting from the center of the US.
    # find the max delay in the dataset

    all_percentages = np.array(data["percentage"])
    per20= np.percentile(all_percentages,20)
    per50= np.percentile(all_percentages,50)
    per90= np.percentile(all_percentages,90)
    # print("percentiles", per20, per50, per90)
    # Separate the coordinates into 2 lists of latitudes and longitudes
    for con in range(len(data)):
    # For each connection number between origin and destination:

        # Get the coordinates for the longitude and latitude for both the origin and destination
        origin=[
            float(data.iloc[con]["origin_latitude"]),
            float(data.iloc[con]["origin_longitude"])
        ]
        destination = [
            float(data.iloc[con]["destination_latitude"]),
            float(data.iloc[con]["destination_longitude"])
        ]
        # Get the iata_code for both origin and destination
        iata_orig=data.iloc[con]["origin"]
        iata_dest=data.iloc[con]["destination"]

        # Build origination point on the map
        folium.Marker(origin,popup=iata_orig, icon=folium.Icon(prefix='fa', icon='plane')).add_to(m)
        # Build destination point on the map
        # folium.Marker(destination,popup="destination", icon_color='white').add_to(m)

        # draw the line between origin and destination?
        folium.PolyLine(
            [origin,destination],
            opacity=0.7,
            color=get_line_color(data.iloc[con]["percentage"],per20,per50,per90),
            tooltip=f'ORIG: {iata_orig} -> DEST: {iata_dest} '
                    f'delay = {data.iloc[con]["percentage"]:.1f}%'
        ).add_to(m)
    return m

    # @ read the series of coordinates and assign them points objects

def main():
    print("testing plot_heatmap_routes")
    print("========================================")
    my_list=[[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
              [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
              [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
              [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
              [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
              [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
              [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]]


    plot_heatmap_routes(my_list)
if __name__ == "__main__":
    main()
