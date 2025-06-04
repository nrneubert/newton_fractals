// src/FractalPlot.tsx
import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

const FractalPlot: React.FC = () => {
  const [data, setData] = useState<number[][][] | null>(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/newton_fractal/')
      .then(res => res.json())
      .then(json => {
        setData(json.rgb);
      })
      .catch(console.error);
  }, []);

  if (!data) return <p>Loading fractal...</p>;

  // Plotly expects a 2D array of [r,g,b] for each pixel
  const image = [{
    z: data,
    type: 'image' as const,
  }];

  return (
    <Plot
      data={image}
      layout={{
        width: 800,
        height: 800,
      }}
      config={{ responsive: true }}
    />
  );
};

export default FractalPlot;
