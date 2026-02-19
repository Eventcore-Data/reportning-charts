/**
 * ChartOptions component for selecting chart type, theme, and format.
 */

import { useState, useEffect } from 'react';
import { Settings, Palette, Plus, X, ChevronDown } from 'lucide-react';
import { getThemes } from '../services/api';

function CollapsibleSection({ id, title, isOpen, onToggle, children }) {
  return (
    <div className="border border-gray-200 rounded-lg">
      <button
        onClick={() => onToggle(id)}
        className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors rounded-lg"
      >
        <span>{title}</span>
        <ChevronDown className={`h-4 w-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      {isOpen && (
        <div className="px-4 pb-4 pt-1">{children}</div>
      )}
    </div>
  );
}

export default function ChartOptions({ options, onOptionsChange }) {
  const [themes, setThemes] = useState(null);
  const [openSections, setOpenSections] = useState({});

  const toggleSection = (key) => {
    setOpenSections(prev => ({ ...prev, [key]: !prev[key] }));
  };

  useEffect(() => {
    loadThemes();
  }, []);

  const loadThemes = async () => {
    try {
      const themesData = await getThemes();
      setThemes(themesData);
    } catch (error) {
      console.error('Failed to load themes:', error);
    }
  };

  const handleChange = (field, value) => {
    onOptionsChange({ ...options, [field]: value });
  };

  const chartTypes = [
    { value: 'auto', label: 'Auto Detect' },
    { value: 'line', label: 'Line Chart' },
    { value: 'bar', label: 'Bar Chart' },
    { value: 'scatter', label: 'Scatter Plot' },
    { value: 'pie', label: 'Pie Chart' },
  ];

  const formats = [
    { value: 'png', label: 'PNG' },
    { value: 'pdf', label: 'PDF' },
    { value: 'svg', label: 'SVG' },
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-2 mb-6">
        <Settings className="h-5 w-5 text-gray-600" />
        <h3 className="text-lg font-semibold text-gray-800">Chart Options</h3>
      </div>

      <div className="space-y-6">
        {/* Chart Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Chart Type
          </label>
          <select
            value={options.chart_type}
            onChange={(e) => handleChange('chart_type', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {chartTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>

        {/* Theme */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <div className="flex items-center space-x-2">
              <Palette className="h-4 w-4" />
              <span>Theme</span>
            </div>
          </label>
          {themes ? (
            <div className="grid grid-cols-2 gap-3">
              {Object.entries(themes.themes).map(([key, theme]) => (
                <button
                  key={key}
                  onClick={() => handleChange('theme', key)}
                  className={`p-3 rounded-lg border-2 transition-all text-left ${
                    options.theme === key
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-medium text-sm text-gray-800">{theme.name}</div>
                  <div className="text-xs text-gray-500 mt-1">{theme.description}</div>
                  <div className="flex space-x-1 mt-2">
                    {theme.colors.slice(0, 5).map((color, idx) => (
                      <div
                        key={idx}
                        className="w-4 h-4 rounded-full border border-gray-200"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="text-sm text-gray-500">Loading themes...</div>
          )}
        </div>

        {/* Format */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Export Format
          </label>
          <div className="flex space-x-2">
            {formats.map((format) => (
              <button
                key={format.value}
                onClick={() => handleChange('format', format.value)}
                className={`flex-1 px-4 py-2 rounded-lg border-2 transition-all ${
                  options.format === format.value
                    ? 'border-blue-500 bg-blue-50 text-blue-700 font-medium'
                    : 'border-gray-200 hover:border-gray-300 text-gray-700'
                }`}
              >
                {format.label}
              </button>
            ))}
          </div>
        </div>

        {/* DPI (for PNG) */}
        {options.format === 'png' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quality (DPI): {options.dpi}
            </label>
            <input
              type="range"
              min="150"
              max="600"
              step="50"
              value={options.dpi}
              onChange={(e) => handleChange('dpi', parseInt(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Low</span>
              <span>Medium</span>
              <span>High</span>
            </div>
          </div>
        )}

        {/* Custom Title */}
        <CollapsibleSection id="title" title="Custom Title" isOpen={openSections.title} onToggle={toggleSection}>
          <input
            type="text"
            value={options.title || ''}
            onChange={(e) => handleChange('title', e.target.value)}
            placeholder="Leave empty for auto-generated title"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </CollapsibleSection>

        {/* Axis Labels */}
        <CollapsibleSection id="axes" title="Axis Labels" isOpen={openSections.axes} onToggle={toggleSection}>
          <div className="grid grid-cols-2 gap-3">
            <input
              type="text"
              value={options.xlabel || ''}
              onChange={(e) => handleChange('xlabel', e.target.value)}
              placeholder="X-axis label"
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={options.ylabel || ''}
              onChange={(e) => handleChange('ylabel', e.target.value)}
              placeholder="Y-axis label"
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </CollapsibleSection>

        {/* Unit Formatting */}
        <CollapsibleSection id="units" title="Axis Unit Formatting" isOpen={openSections.units} onToggle={toggleSection}>
          <div className="grid grid-cols-2 gap-3">
            <input
              type="text"
              value={options.unit_x_prefix}
              onChange={(e) => handleChange('unit_x_prefix', e.target.value)}
              placeholder="X prefix (e.g. $)"
              className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={options.unit_x_suffix}
              onChange={(e) => handleChange('unit_x_suffix', e.target.value)}
              placeholder="X suffix (e.g. %)"
              className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={options.unit_y_prefix}
              onChange={(e) => handleChange('unit_y_prefix', e.target.value)}
              placeholder="Y prefix (e.g. $)"
              className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="text"
              value={options.unit_y_suffix}
              onChange={(e) => handleChange('unit_y_suffix', e.target.value)}
              placeholder="Y suffix (e.g. kg)"
              className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </CollapsibleSection>

        {/* Data Labels */}
        <CollapsibleSection id="dataLabels" title="Data Labels" isOpen={openSections.dataLabels} onToggle={toggleSection}>
          <div className="flex items-center justify-between mb-2">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={options.show_data_labels}
                onChange={(e) => handleChange('show_data_labels', e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-600">Show values</span>
            </label>
          </div>
          {options.show_data_labels && (
            <input
              type="text"
              value={options.data_label_format}
              onChange={(e) => handleChange('data_label_format', e.target.value)}
              placeholder="Format (e.g. ,.0f for thousands)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          )}
        </CollapsibleSection>

        {/* Grid Controls */}
        <CollapsibleSection id="grid" title="Grid Lines" isOpen={openSections.grid} onToggle={toggleSection}>
          <div className="flex items-center justify-between mb-2">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={options.grid_enabled}
                onChange={(e) => handleChange('grid_enabled', e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-600">Show grid</span>
            </label>
          </div>
          {options.grid_enabled && (
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Style</label>
                <select
                  value={options.grid_linestyle}
                  onChange={(e) => handleChange('grid_linestyle', e.target.value)}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="solid">Solid</option>
                  <option value="dashed">Dashed</option>
                  <option value="dotted">Dotted</option>
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">
                  Opacity: {options.grid_alpha || 'Theme default'}
                </label>
                <input
                  type="range"
                  min="0.1"
                  max="1.0"
                  step="0.1"
                  value={options.grid_alpha || 0.3}
                  onChange={(e) => handleChange('grid_alpha', e.target.value)}
                  className="w-full"
                />
              </div>
            </div>
          )}
        </CollapsibleSection>

        {/* Font Controls */}
        <CollapsibleSection id="fonts" title="Fonts" isOpen={openSections.fonts} onToggle={toggleSection}>
          <select
            value={options.font_family}
            onChange={(e) => handleChange('font_family', e.target.value)}
            className="w-full px-4 py-2 mb-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Theme Default</option>
            <option value="sans-serif">Sans-serif</option>
            <option value="serif">Serif</option>
            <option value="monospace">Monospace</option>
          </select>
          <div className="grid grid-cols-3 gap-2">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Title size</label>
              <input
                type="number"
                value={options.font_title_size}
                onChange={(e) => handleChange('font_title_size', e.target.value)}
                placeholder="16"
                min="8"
                max="48"
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Label size</label>
              <input
                type="number"
                value={options.font_label_size}
                onChange={(e) => handleChange('font_label_size', e.target.value)}
                placeholder="12"
                min="6"
                max="36"
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Tick size</label>
              <input
                type="number"
                value={options.font_tick_size}
                onChange={(e) => handleChange('font_tick_size', e.target.value)}
                placeholder="10"
                min="6"
                max="36"
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </CollapsibleSection>

        {/* Custom Colors */}
        <CollapsibleSection id="colors" title="Custom Colors" isOpen={openSections.colors} onToggle={toggleSection}>
          {options.colors.length === 0 && (
            <p className="text-xs text-gray-500 mb-2">Using theme colors. Add colors to override.</p>
          )}
          <div className="space-y-2">
            {options.colors.map((color, idx) => (
              <div key={idx} className="flex items-center space-x-2">
                <input
                  type="color"
                  value={color}
                  onChange={(e) => {
                    const newColors = [...options.colors];
                    newColors[idx] = e.target.value;
                    handleChange('colors', newColors);
                  }}
                  className="w-10 h-10 rounded border border-gray-300 cursor-pointer"
                />
                <span className="text-sm text-gray-600 font-mono">{color}</span>
                <button
                  onClick={() => {
                    const newColors = options.colors.filter((_, i) => i !== idx);
                    handleChange('colors', newColors);
                  }}
                  className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
          <button
            onClick={() => handleChange('colors', [...options.colors, '#2E86AB'])}
            className="mt-2 flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            <Plus className="h-4 w-4" />
            <span>Add Color</span>
          </button>
        </CollapsibleSection>
      </div>
    </div>
  );
}
