# World Population Animation 🌍

Interactive visualization of global population changes over time using Python and Plotly.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Plotly](https://img.shields.io/badge/Plotly-5.18-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features ✨

- 📊 Interactive world map with time slider animation
- 🎨 Multiple visualization modes (choropleth, bubble map)
- 🔍 Hover tooltips with detailed country statistics
- 📈 Population growth rate calculations
- 💾 Export to HTML for sharing
- 🧹 Clean, modular OOP code structure

## Data Source

Population data from [World Bank Open Data](https://data.worldbank.org/) (1960-2023)

## Installation 🚀
```bash
# Clone the repository
git clone https://github.com/ggittasseruwagi/world-population-animation.git
cd world-population-animation

# Install dependencies
pip install -r requirements.txt
```

## Usage 📝

### Jupyter Notebook (Interactive)
```bash
jupyter notebook
# Open population_viz.ipynb
```

### Python Script (Coming Soon)
```bash
python main.py
```

## Quick Start Example
```python
from src.data_loader import DataLoader
from src.visualizer import MapVisualizer

# Load data
loader = DataLoader()
loader.fetch_population_data(start_year=1960, end_year=2023)
df = loader.clean_data()

# Create visualization
viz = MapVisualizer(df)
viz.create_choropleth_map(color_mode='population')
viz.show()

# Save as HTML
viz.save_html('my_population_map.html')
```

## Project Structure 📁
```
world-population-animation/
├── README.md
├── requirements.txt
├── .gitignore
├── population_viz.ipynb      # Main Jupyter notebook
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # DataLoader class
│   └── visualizer.py         # MapVisualizer class
└── data/                     # Downloaded data (git-ignored)
```

## Visualization Modes 🎨

1. **Choropleth Map (Population)** - Countries colored by total population
2. **Choropleth Map (Growth Rate)** - Countries colored by population growth rate
3. **Bubble Map** - Bubble size represents population

## Future Enhancements 🔮

- [ ] Add population projection data (2024-2100)
- [ ] Migration pattern visualization
- [ ] Comparative country analysis
- [ ] Export as MP4/GIF animation
- [ ] Custom region filtering

## Technologies Used 🛠️

- **Python 3.13** - Programming language
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **World Bank API** - Population data source

## Contributing 🤝

Contributions welcome! Feel free to open issues or submit pull requests.

## License 📄

MIT License - feel free to use this project for learning and personal projects!

## Author ✍️

Created during a 2-hour live coding stream on YouTube!

---

⭐ Star this repo if you found it helpful!
