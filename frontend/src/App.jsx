/**
 * Main App component for Excel Chart Maker.
 */

import { useState } from 'react';
import { BarChart3 } from 'lucide-react';
import FileUpload from './components/FileUpload';
import DataTable from './components/DataTable';
import ChartOptions from './components/ChartOptions';
import ChartPreview from './components/ChartPreview';
import DownloadButton from './components/DownloadButton';
import { uploadFile, generateChart } from './services/api';

function App() {
  // State management
  const [fileId, setFileId] = useState(null);
  const [filename, setFilename] = useState(null);
  const [dataPreview, setDataPreview] = useState(null);
  const [chartOptions, setChartOptions] = useState({
    chart_type: 'auto',
    theme: 'professional',
    format: 'png',
    dpi: 300,
    title: '',
    xlabel: '',
    ylabel: '',
    grid_enabled: true,
    grid_linestyle: 'solid',
    grid_alpha: '',
    font_family: '',
    font_title_size: '',
    font_label_size: '',
    font_tick_size: '',
    unit_x_prefix: '',
    unit_x_suffix: '',
    unit_y_prefix: '',
    unit_y_suffix: '',
    show_data_labels: false,
    data_label_format: '',
    colors: [],
  });
  const [chartData, setChartData] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [generateError, setGenerateError] = useState(null);

  // Handle file upload
  const handleFileUpload = async (file) => {
    setIsUploading(true);
    setUploadError(null);
    setChartData(null); // Reset chart when new file uploaded

    try {
      const response = await uploadFile(file);
      setFileId(response.file_id);
      setFilename(response.filename);
      setDataPreview(response.data_preview);
    } catch (error) {
      console.error('Upload error:', error);
      setUploadError(
        error.response?.data?.detail || 'Failed to upload file. Please try again.'
      );
    } finally {
      setIsUploading(false);
    }
  };

  // Handle chart generation
  const handleGenerateChart = async () => {
    if (!fileId) return;

    setIsGenerating(true);
    setGenerateError(null);

    try {
      const request = {
        file_id: fileId,
        chart_type: chartOptions.chart_type,
        theme: chartOptions.theme,
        format: chartOptions.format,
        dpi: chartOptions.dpi,
        title: chartOptions.title || null,
        xlabel: chartOptions.xlabel || null,
        ylabel: chartOptions.ylabel || null,
        colors: chartOptions.colors.length > 0 ? chartOptions.colors : null,
      };

      // Only include nested objects when non-default
      if (!chartOptions.grid_enabled || chartOptions.grid_linestyle !== 'solid' || chartOptions.grid_alpha) {
        request.grid = {
          enabled: chartOptions.grid_enabled,
          linestyle: chartOptions.grid_linestyle,
          alpha: chartOptions.grid_alpha ? parseFloat(chartOptions.grid_alpha) : null,
        };
      }

      if (chartOptions.font_family || chartOptions.font_title_size || chartOptions.font_label_size || chartOptions.font_tick_size) {
        request.fonts = {
          family: chartOptions.font_family || null,
          title_size: chartOptions.font_title_size ? parseInt(chartOptions.font_title_size) : null,
          label_size: chartOptions.font_label_size ? parseInt(chartOptions.font_label_size) : null,
          tick_size: chartOptions.font_tick_size ? parseInt(chartOptions.font_tick_size) : null,
        };
      }

      if (chartOptions.unit_x_prefix || chartOptions.unit_x_suffix || chartOptions.unit_y_prefix || chartOptions.unit_y_suffix) {
        request.units = {
          x_prefix: chartOptions.unit_x_prefix,
          x_suffix: chartOptions.unit_x_suffix,
          y_prefix: chartOptions.unit_y_prefix,
          y_suffix: chartOptions.unit_y_suffix,
        };
      }

      if (chartOptions.show_data_labels) {
        request.data_labels = {
          show: true,
          format: chartOptions.data_label_format || null,
        };
      }

      const response = await generateChart(request);
      setChartData(response);
    } catch (error) {
      console.error('Generation error:', error);
      setGenerateError(
        error.response?.data?.detail || 'Failed to generate chart. Please try again.'
      );
    } finally {
      setIsGenerating(false);
    }
  };

  // Reset state for new upload
  const handleReset = () => {
    setFileId(null);
    setFilename(null);
    setDataPreview(null);
    setChartData(null);
    setUploadError(null);
    setGenerateError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-600 rounded-lg">
              <BarChart3 className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Excel Chart Maker</h1>
              <p className="text-sm text-gray-600 mt-1">
                Create publication-ready charts from Excel files
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Step 1: File Upload */}
          <section>
            <div className="mb-4">
              <h2 className="text-xl font-semibold text-gray-800 flex items-center space-x-2">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white text-sm font-bold">
                  1
                </span>
                <span>Upload Excel File</span>
              </h2>
            </div>
            <FileUpload
              onFileUpload={handleFileUpload}
              isUploading={isUploading}
              error={uploadError}
            />
            {filename && (
              <div className="mt-4 flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center space-x-2">
                  <span className="text-green-600 text-xl">✓</span>
                  <span className="text-sm font-medium text-green-800">
                    Uploaded: {filename}
                  </span>
                </div>
                <button
                  onClick={handleReset}
                  className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                  Upload Different File
                </button>
              </div>
            )}
          </section>

          {/* Step 2: Data Preview */}
          {dataPreview && (
            <section>
              <div className="mb-4">
                <h2 className="text-xl font-semibold text-gray-800 flex items-center space-x-2">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white text-sm font-bold">
                    2
                  </span>
                  <span>Review Data</span>
                </h2>
              </div>
              <DataTable dataPreview={dataPreview} />
            </section>
          )}

          {/* Step 3: Chart Options & Generation */}
          {dataPreview && (
            <section>
              <div className="mb-4">
                <h2 className="text-xl font-semibold text-gray-800 flex items-center space-x-2">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white text-sm font-bold">
                    3
                  </span>
                  <span>Configure & Generate</span>
                </h2>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Options */}
                <div className="lg:col-span-1">
                  <ChartOptions options={chartOptions} onOptionsChange={setChartOptions} />
                  <button
                    onClick={handleGenerateChart}
                    disabled={isGenerating || !fileId}
                    className={`w-full mt-4 flex items-center justify-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all ${
                      isGenerating || !fileId
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg'
                    }`}
                  >
                    {isGenerating ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        <span>Generating...</span>
                      </>
                    ) : (
                      <>
                        <BarChart3 className="h-5 w-5" />
                        <span>Generate Chart</span>
                      </>
                    )}
                  </button>
                </div>

                {/* Preview */}
                <div className="lg:col-span-2">
                  <ChartPreview
                    chartData={chartData}
                    isLoading={isGenerating}
                    error={generateError}
                  />
                </div>
              </div>
            </section>
          )}

          {/* Step 4: Download */}
          {chartData && (
            <section>
              <div className="mb-4">
                <h2 className="text-xl font-semibold text-gray-800 flex items-center space-x-2">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600 text-white text-sm font-bold">
                    4
                  </span>
                  <span>Download</span>
                </h2>
              </div>
              <div className="max-w-md">
                <DownloadButton chartData={chartData} />
              </div>
            </section>
          )}
        </div>
      </main>


    </div>
  );
}

export default App;
