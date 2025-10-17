"""
Visualization module for world population maps
"""
import plotly.express as px


class MapVisualizer:
    """
    Creates interactive map visualizations of population data using Plotly.
    """

    def __init__(self, data):
        """Initialize visualizer with cleaned data"""
        self.data = data
        self.fig = None

    def prepare_data_for_viz(self):
        """Prepare data with additional calculated fields"""
        df = self.data.copy()
        df['population_millions'] = df['population'] / 1_000_000

        df = df.sort_values(['country_code', 'year'])
        df['population_change'] = df.groupby('country_code')['population'].pct_change() * 100
        df['population_change'] = df['population_change'].fillna(0)

        print(f"✅ Data prepared for visualization")
        return df

    def create_choropleth_map(self, color_mode='population'):
        """Create an animated choropleth map"""
        df = self.prepare_data_for_viz()

        print(f"🎨 Creating choropleth map (color mode: {color_mode})...")

        if color_mode == 'population':
            color_column = 'population_millions'
            color_label = 'Population (Millions)'
            color_scale = 'Viridis'
        elif color_mode == 'growth':
            color_column = 'population_change'
            color_label = 'Population Growth Rate (%)'
            color_scale = 'RdYlGn'
        else:
            color_column = 'population_millions'
            color_label = 'Population (Millions)'
            color_scale = 'Viridis'

        hover_template = (
            '<b>%{hovertext}</b><br>'
            'Year: %{customdata[0]}<br>'
            'Population: %{customdata[1]:,.0f}<br>'
            'Growth Rate: %{customdata[2]:.2f}%<br>'
            '<extra></extra>'
        )

        df['custom_year'] = df['year']
        df['custom_pop'] = df['population']
        df['custom_growth'] = df['population_change']

        self.fig = px.choropleth(
            df,
            locations='country_code',
            color=color_column,
            hover_name='country',
            animation_frame='year',
            color_continuous_scale=color_scale,
            labels={color_column: color_label},
            title=f'World Population Visualization ({df["year"].min()}-{df["year"].max()})',
            custom_data=['custom_year', 'custom_pop', 'custom_growth']
        )

        self.fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            ),
            height=700,
            title_font_size=24,
            title_x=0.5,
            coloraxis_colorbar=dict(
                title=color_label,
                thickness=20,
                len=0.7
            )
        )

        self.fig.update_traces(hovertemplate=hover_template)

        self.fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 300
        self.fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 200

        print(f"✅ Map created successfully!")
        return self.fig

    def create_bubble_map(self):
        """Create an animated bubble map"""
        df = self.prepare_data_for_viz()

        print(f"🎨 Creating bubble map...")

        self.fig = px.scatter_geo(
            df,
            locations='country_code',
            color='population_millions',
            hover_name='country',
            size='population_millions',
            animation_frame='year',
            projection='natural earth',
            title=f'World Population (Bubble Size) - {df["year"].min()}-{df["year"].max()}',
            color_continuous_scale='Plasma',
            size_max=50
        )

        self.fig.update_layout(
            height=700,
            title_font_size=24,
            title_x=0.5
        )

        print(f"✅ Bubble map created successfully!")
        return self.fig

    def show(self):
        """Display the visualization"""
        if self.fig is None:
            print("❌ No visualization created yet!")
            return

        self.fig.show()

    def save_html(self, filename='world_population_viz.html'):
        """Save the visualization as an HTML file"""
        if self.fig is None:
            print("❌ No visualization created yet!")
            return

        self.fig.write_html(filename)
        print(f"✅ Visualization saved as '{filename}'")
