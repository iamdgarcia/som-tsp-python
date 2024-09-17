import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

def visualize_network(city_data, neuron_positions, output_file='diagram.png', ax=None):
    """Create a visual representation of the network using an aesthetic color palette."""
    mpl.rcParams['agg.path.chunksize'] = 10000
    sns.set_style('white')

    # Select a Seaborn color palette
    color_palette = sns.color_palette('muted')

    if ax is None:
        fig = plt.figure(figsize=(5, 5), frameon=False)
        plot_axis = fig.add_axes([0, 0, 1, 1])

        plot_axis.set_aspect('equal', adjustable='datalim')
        plt.axis('off')
        # Set background color to white
        fig.patch.set_facecolor('white')
        plot_axis.set_facecolor('white')

        # Plot city points and neuron path
        plot_axis.scatter(city_data['x'], city_data['y'], color=color_palette[0], s=4)
        plot_axis.plot(neuron_positions[:, 0], neuron_positions[:, 1], marker='.', linestyle='-', color=color_palette[1], markersize=2)

        plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=200)
        plt.close()
    else:
        ax.scatter(city_data['x'], city_data['y'], color=color_palette[0], s=4)
        ax.plot(neuron_positions[:, 0], neuron_positions[:, 1], marker='.', linestyle='-', color=color_palette[1], markersize=2)
        return ax

def visualize_route(city_data, city_route, output_file='diagram.png', ax=None):
    """Generate a visual representation of the route using an aesthetic color palette."""
    mpl.rcParams['agg.path.chunksize'] = 10000
    sns.set_style('white')

    # Select a Seaborn color palette
    color_palette = sns.color_palette('muted')

    if ax is None:
        fig = plt.figure(figsize=(5, 5), frameon=False)
        plot_axis = fig.add_axes([0, 0, 1, 1])

        plot_axis.set_aspect('equal', adjustable='datalim')
        plt.axis('off')

        # Plot cities and route path
        plot_axis.scatter(city_data['x'], city_data['y'], color=color_palette[0], s=4)
        ordered_route = city_data.reindex(city_route)
        ordered_route.loc[ordered_route.shape[0]] = ordered_route.iloc[0]
        plot_axis.plot(ordered_route['x'], ordered_route['y'], color=color_palette[2], linewidth=1)

        plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=200)
        plt.close()
    else:
        ax.scatter(city_data['x'], city_data['y'], color=color_palette[0], s=4)
        ordered_route = city_data.reindex(city_route)
        ordered_route.loc[ordered_route.shape[0]] = ordered_route.iloc[0]
        ax.plot(ordered_route['x'], ordered_route['y'], color=color_palette[2], linewidth=1)
        return ax
