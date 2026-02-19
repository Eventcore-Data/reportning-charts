/**
 * ChartPreview component to display generated chart.
 */

import { Eye, Loader } from 'lucide-react';

/**
 * Build proper data URI for different chart formats
 */
const buildDataUri = (base64, format) => {
  try {
    switch (format) {
      case 'png':
        return `data:image/png;base64,${base64}`;

      case 'pdf':
        return `data:application/pdf;base64,${base64}`;

      case 'svg':
        // Decode base64 to get SVG string
        const svgString = atob(base64);
        // URL encode for data URI (charset=utf-8 for proper rendering)
        const encodedSvg = encodeURIComponent(svgString);
        return `data:image/svg+xml;charset=utf-8,${encodedSvg}`;

      default:
        return `data:application/octet-stream;base64,${base64}`;
    }
  } catch (error) {
    console.error('Error building data URI:', error);
    return null;
  }
};

export default function ChartPreview({ chartData, isLoading, error }) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12">
        <div className="flex flex-col items-center justify-center space-y-4">
          <Loader className="h-12 w-12 text-blue-500 animate-spin" />
          <div className="text-center">
            <p className="text-lg font-medium text-gray-700">Generating your chart...</p>
            <p className="text-sm text-gray-500 mt-1">This may take a few moments</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-red-200 p-6">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-100 mb-4">
            <span className="text-2xl">⚠️</span>
          </div>
          <h3 className="text-lg font-semibold text-red-800 mb-2">Generation Failed</h3>
          <p className="text-sm text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  if (!chartData) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12">
        <div className="flex flex-col items-center justify-center space-y-4 text-gray-400">
          <Eye className="h-16 w-16" />
          <div className="text-center">
            <p className="text-lg font-medium">No chart yet</p>
            <p className="text-sm mt-1">Configure options and click "Generate Chart"</p>
          </div>
        </div>
      </div>
    );
  }

  // Render PNG format (current working approach)
  const renderPngPreview = (dataUri) => (
    <img
      src={dataUri}
      alt="Generated Chart"
      className="max-w-full h-auto rounded-lg shadow-md"
    />
  );

  // Render SVG format
  const renderSvgPreview = (dataUri) => (
    <img
      src={dataUri}
      alt="Generated Chart"
      className="max-w-full h-auto rounded-lg shadow-md"
    />
  );

  // Render PDF format with embed
  const renderPdfPreview = (dataUri) => (
    <div className="w-full">
      <embed
        src={dataUri}
        type="application/pdf"
        width="100%"
        height="600px"
        className="rounded-lg shadow-md border border-gray-200"
      />
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-xs text-blue-800 text-center">
          💡 If the PDF doesn't display properly, use the download button below to view it in your PDF viewer.
        </p>
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Eye className="h-5 w-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-800">Chart Preview</h3>
          </div>
          <span className="text-xs font-medium text-gray-500 uppercase px-2 py-1 bg-gray-200 rounded">
            {chartData.format}
          </span>
        </div>
      </div>
      <div className="p-6">
        <div className="flex justify-center">
          {(() => {
            const dataUri = buildDataUri(chartData.chart_base64, chartData.format);

            if (!dataUri) {
              return (
                <div className="text-center p-8 text-gray-500">
                  <p className="text-sm">Unable to generate preview.</p>
                  <p className="text-xs mt-1">Please use the download button to view your chart.</p>
                </div>
              );
            }

            switch (chartData.format) {
              case 'png':
                return renderPngPreview(dataUri);
              case 'svg':
                return renderSvgPreview(dataUri);
              case 'pdf':
                return renderPdfPreview(dataUri);
              default:
                return (
                  <div className="text-center p-8 text-gray-500">
                    <p className="text-sm">Preview not available for {chartData.format} format.</p>
                    <p className="text-xs mt-1">Please download to view your chart.</p>
                  </div>
                );
            }
          })()}
        </div>
      </div>
    </div>
  );
}
