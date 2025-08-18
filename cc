<!-- SECTION 1: HTML CHANGES -->
<!-- Replace the existing Axis Labels section (around line 303-313) with this: -->

<div class="section">
    <h3>Axis Labels</h3>
    <input class="input-field" id="xAxisTitle" placeholder="X-Axis Title">
    <input class="input-field" id="yAxisTitle" placeholder="Y-Axis Title">
    
    <div class="input-group">
        <input class="input-field" id="yPrefix" placeholder="Y-Prefix">
        <input class="input-field" id="ySuffix" placeholder="Y-Suffix">
    </div>
    
    <!-- New radio button group for Top Only mode -->
    <div style="margin-top: 12px;">
        <label style="display: block; color: #a8a8a8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; font-weight: 600;">Prefix & Suffix at Top Only</label>
        <div class="radio-group">
            <label class="radio-label">
                <input type="radio" name="prefixSuffixTopOnly" value="off" checked>
                Off
            </label>
            <label class="radio-label">
                <input type="radio" name="prefixSuffixTopOnly" value="on">
                On
            </label>
        </div>
    </div>
    
    <div style="margin-top: 12px;">
        <label style="display: block; color: #a8a8a8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; font-weight: 600;">Y-Axis Denominator</label>
        <input class="input-field" placeholder="eg. 100; 1,000,000">
    </div>
</div>

<!-- REMOVE this from Display Options section (around line 336-344): -->
<!-- DELETE THIS BLOCK:
<div class="display-option">
    <span>Y-Axis Labels</span>
    <select class="dropdown">
        <option>On</option>
        <option>Off</option>
        <option>Top Only</option>
    </select>
</div>
-->

<!-- SECTION 2: JAVASCRIPT CHANGES -->
<script>
// Add this CSS for disabled radio state (add to existing <style> section around line 100)
const additionalStyles = `
    .radio-group.disabled {
        opacity: 0.5;
        pointer-events: none;
    }
    
    .radio-label.disabled {
        cursor: not-allowed;
        color: #666;
    }
`;

// UPDATE generateChart function (replace existing around line 1685)
async function generateChart() {
    if (!currentData.length) {
        showStatus('❌ No data available. Please upload a file first.', 'error');
        return;
    }
    
    const chartType = getSelectedChartType();
    const xColumn = document.getElementById('xColumn').value;
    const yColumn = document.getElementById('yColumn').value;
    const zColumn = document.getElementById('zColumn').value;
    const colorColumn = document.getElementById('colorColumn').value;
    const autoSpacing = document.getElementById('autoSpacing').checked;
    const horizontalGrid = document.getElementById('horizontalGrid').checked;
    const verticalGrid = document.getElementById('verticalGrid').checked;
    const title = getFieldById('chartTitle') ? getFieldById('chartTitle').value : `${chartType.charAt(0).toUpperCase() + chartType.slice(1)} Chart`;
    const subtitle = getFieldById('chartSubtitle') ? getFieldById('chartSubtitle').value : '';
    const footnote = getFieldById('chartFootnote') ? getFieldById('chartFootnote').value : '';
    const source = getFieldById('chartSource') ? getFieldById('chartSource').value : '';
    const xAxisTitle = document.getElementById('xAxisTitle') ? document.getElementById('xAxisTitle').value : '';
    const yAxisTitle = document.getElementById('yAxisTitle') ? document.getElementById('yAxisTitle').value : '';
    
    // NEW: Get prefix/suffix values and top-only mode
    const yPrefix = document.getElementById('yPrefix').value || '';
    const ySuffix = document.getElementById('ySuffix').value || '';
    const topOnlyMode = document.querySelector('input[name="prefixSuffixTopOnly"]:checked').value;
    const hasPrefixOrSuffix = yPrefix.length > 0 || ySuffix.length > 0;
    
    if (!xColumn || (!yColumn && !['pie', 'histogram'].includes(chartType))) {
        showStatus('❌ Please select the required columns for your chart.', 'error');
        return;
    }
    
    try {
        showLoading(true);
        showStatus('🎨 Generating your interactive chart...', 'warning');
        
        const { topMargin, bottomMargin } = calculateDynamicMargins(title, subtitle, footnote, source);
        const containerHeight = calculateContainerHeight(topMargin, bottomMargin);
        
        const chartContainer = document.getElementById('chartContainer');
        chartContainer.style.height = `${containerHeight}px`;
        chartContainer.style.minHeight = 'unset';
        
        processedData = prepareChartData();
        showDataPreview(processedData);
        
        let plotlyConfig = createPlotlyConfig(chartType, processedData, {
            xColumn,
            yColumn,
            zColumn,
            colorColumn,
            title,
            subtitle,
            footnote,
            source,
            horizontalGrid,
            verticalGrid,
            topMargin,
            bottomMargin,
            xAxisTitle,
            yAxisTitle,
            yPrefix,
            ySuffix,
            topOnlyMode,
            hasPrefixOrSuffix
        });
        
        // Handle "Top Only" mode with server call
        if (hasPrefixOrSuffix && topOnlyMode === 'on') {
            try {
                const yData = processedData.map(row => row[yColumn]).filter(v => !isNaN(v));
                
                const response = await fetch(`${API_ENDPOINT}/api/format-top-tick`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        values: yData,
                        prefix: yPrefix,
                        suffix: ySuffix,
                        chart_type: chartType,
                        axis: chartType === 'horizontal_bar' ? 'x' : 'y'
                    })
                });
                
                if (response.ok) {
                    const tickData = await response.json();
                    
                    // Apply the server-calculated tick configuration
                    if (chartType === 'horizontal_bar') {
                        plotlyConfig.layout.xaxis = {
                            ...plotlyConfig.layout.xaxis,
                            tickmode: 'array',
                            tickvals: tickData.tickvals,
                            ticktext: tickData.ticktext
                        };
                        // Remove any prefix/suffix that might have been added
                        delete plotlyConfig.layout.xaxis.tickprefix;
                        delete plotlyConfig.layout.xaxis.ticksuffix;
                    } else {
                        plotlyConfig.layout.yaxis = {
                            ...plotlyConfig.layout.yaxis,
                            tickmode: 'array',
                            tickvals: tickData.tickvals,
                            ticktext: tickData.ticktext
                        };
                        // Remove any prefix/suffix that might have been added
                        delete plotlyConfig.layout.yaxis.tickprefix;
                        delete plotlyConfig.layout.yaxis.ticksuffix;
                    }
                    
                    console.log('Top-only labels applied successfully');
                }
            } catch (error) {
                console.warn('Top-only mode failed, using standard mode:', error);
                // Fall back to standard mode (all labels)
            }
        }
        
        // Continue with existing auto-spacing code if needed
        if (autoSpacing) {
            try {
                const xData = processedData.map(row => row[xColumn]);
                const spacingResponse = await fetch(`${API_ENDPOINT}/api/auto-spacing`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        x_labels: xData,
                        chart_type: chartType
                    })
                });
                
                if (spacingResponse.ok) {
                    const spacingData = await spacingResponse.json();
                    if (spacingData.success) {
                        plotlyConfig.layout.xaxis = {
                            ...plotlyConfig.layout.xaxis,
                            ...spacingData.xaxis_config,
                            showgrid: verticalGrid,
                            showline: true,
                            linecolor: 'rgba(255,255,255,0.3)',
                            linewidth: 1
                        };
                    }
                }
            } catch (error) {
                console.warn('Auto-spacing failed, using default spacing:', error);
            }
        }
        
        const plotlyChart = document.getElementById('plotlyChart');
        if (plotlyChart) {
            plotlyChart.innerHTML = '';
            Plotly.newPlot('plotlyChart', plotlyConfig.data, plotlyConfig.layout, plotlyConfig.config)
                .then(function() {
                    syncContainerWithPlotly();
                    measureChartDimensions();
                    validateAndAdjustChartSpacing();
                    setupAxisTitleListeners();
                });
        }
        
        if (chartContainer) {
            chartContainer.classList.add('has-chart');
        }
        
        showStatus(`✅ Interactive chart generated successfully! Showing ${processedData.length} data points.`, 'success');
        
    } catch (error) {
        showStatus(`❌ Error generating chart: ${error.message}`, 'error');
        console.error('Chart generation error:', error);
    } finally {
        showLoading(false);
    }
}

// UPDATE createPlotlyConfig function (replace existing around line 1851)
function createPlotlyConfig(chartType, data, options) {
    const { 
        xColumn, yColumn, zColumn, colorColumn, 
        title, subtitle, footnote, source, 
        horizontalGrid, verticalGrid, 
        topMargin, bottomMargin, 
        xAxisTitle, yAxisTitle,
        yPrefix, ySuffix, topOnlyMode, hasPrefixOrSuffix
    } = options;
    
    const xData = data.map(row => row[xColumn]);
    const yData = yColumn ? data.map(row => row[yColumn]) : [];
    const zData = zColumn ? data.map(row => row[zColumn]) : [];
    const colorData = colorColumn ? data.map(row => row[colorColumn]) : [];
    
    let plotData = [];
    
    let titleText = title || '';
    if (subtitle) {
        const wrappedSubtitle = wrapSubtitleText(subtitle);
        titleText = `${title}<br><span style="font-size: 14px; color: rgba(255,255,255,0.8);">${wrappedSubtitle}</span>`;
    }
    
    let layout = {
        title: {
            text: titleText,
            font: { size: 18, color: 'white' },
            x: 0.5,
            xanchor: 'center'
        },
        showlegend: true,
        margin: { 
            t: topMargin,
            b: bottomMargin, 
            l: 80,
            r: 50
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: 'white' },
        height: 400 + topMargin + bottomMargin,
        width: 850,
        autosize: false
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToAdd: ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape'],
        displaylogo: false
    };
    
    // Helper function to apply prefix/suffix based on mode
    function applyPrefixSuffix(axisConfig, isValueAxis) {
        if (!isValueAxis) return axisConfig;
        
        // Only apply if there's a prefix or suffix and topOnlyMode is 'off'
        if (hasPrefixOrSuffix && topOnlyMode === 'off') {
            axisConfig.tickprefix = yPrefix;
            axisConfig.ticksuffix = ySuffix;
        }
        // Note: topOnlyMode === 'on' is handled by server call in generateChart
        
        return axisConfig;
    }
    
    switch (chartType) {
        case 'vertical_bar':
            plotData = [{
                type: 'bar',
                x: xData,
                y: yData,
                orientation: 'v',
                marker: {
                    color: colorData.length ? colorData : '#e94560',
                    colorscale: colorData.length ? 'Viridis' : undefined,
                    showscale: colorData.length > 0
                },
                name: yColumn || 'Values'
            }];
            
            layout.xaxis = applyGridSettings({
                title: xAxisTitle || xColumn,
                gridcolor: 'rgba(255,255,255,0.1)',
                color: 'white',
                range: [-0.5, xData.length - 0.5]
            }, verticalGrid, horizontalGrid);
            
            layout.yaxis = applyPrefixSuffix(applyGridSettings({
                title: yAxisTitle || yColumn || 'Value',
                gridcolor: 'rgba(255,255,255,0.1)',
                color: 'white',
                zeroline: true,
                zerolinecolor: 'gray',
                zerolinewidth: 2,
                range: [0, Math.max(...yData) * 1.1]
            }, horizontalGrid, verticalGrid), true);
            break;
            
        case 'horizontal_bar':
            plotData = [{
                type: 'bar',
                x: yData,
                y: xData,
                orientation: 'h',
                marker: {
                    color: colorData.length ? colorData : '#e94560',
                    colorscale: colorData.length ? 'Viridis' : undefined,
                    showscale: colorData.length > 0
                },
                name: yColumn || 'Values'
            }];
            
            // For horizontal bar, apply to X-axis (which shows values)
            layout.xaxis = applyPrefixSuffix(applyGridSettings({
                title: yAxisTitle || yColumn || 'Value',
                gridcolor: 'rgba(255,255,255,0.1)',
                color: 'white',
                range: [0, Math.max(...yData) * 1.1]
            }, horizontalGrid, verticalGrid), true);
            
            layout.yaxis = applyGridSettings({
                title: xAxisTitle || xColumn,
                gridcolor: 'rgba(255,255,255,0.1)',
                color: 'white',
                zeroline: true,
                zerolinecolor: 'gray',
                zerolinewidth: 2
            }, verticalGrid, horizontalGrid);
            break;
            
        case 'line':
            plotData = [{
                type: 'scatter',
                mode: 'lines+markers',
                x: xData,
                y: yData,
                line: { color: '#e94560', width: 3 },
                marker: { size: 6, color: '#e94560' },
                name: yColumn || 'Values'
            }];
            
            layout.xaxis = applyGridSettings({ 
                title: xAxisTitle || xColumn, 
                gridcolor: 'rgba(255,255,255,0.1)', 
                color: 'white',
                range: [-0.5, xData.length - 0.5]
            }, verticalGrid, horizontalGrid);
            
            layout.yaxis = applyPrefixSuffix(applyGridSettings({ 
                title: yAxisTitle || yColumn || 'Value', 
                gridcolor: 'rgba(255,255,255,0.1)', 
                color: 'white', 
                zeroline: true, 
                zerolinecolor: 'gray', 
                zerolinewidth: 2, 
                range: [0, Math.max(...yData) * 1.1] 
            }, horizontalGrid, verticalGrid), true);
            break;
            
        case 'scatter':
            plotData = [{
                type: 'scatter',
                mode: 'markers',
                x: xData,
                y: yData,
                marker: {
                    size: 8,
                    color: colorData.length ? colorData : '#e94560',
                    colorscale: colorData.length ? 'Viridis' : undefined,
                    showscale: colorData.length > 0,
                    colorbar: colorData.length ? { title: colorColumn } : undefined
                },
                text: colorData.length ? colorData.map((val, i) => `${xColumn}: ${xData[i]}<br>${yColumn}: ${yData[i]}<br>${colorColumn}: ${val}`) : undefined,
                hovertemplate: colorData.length ? '%{text}<extra></extra>' : undefined,
                name: 'Data Points'
            }];
            
            layout.xaxis = applyGridSettings({ 
                title: xAxisTitle || xColumn, 
                gridcolor: 'rgba(255,255,255,0.1)', 
                color: 'white',
                range: [-0.5, xData.length - 0.5]
            }, verticalGrid, horizontalGrid);
            
            layout.yaxis = applyPrefixSuffix(applyGridSettings({ 
                title: yAxisTitle || yColumn, 
                gridcolor: 'rgba(255,255,255,0.1)', 
                color: 'white', 
                zeroline: true, 
                zerolinecolor: 'gray', 
                zerolinewidth: 2, 
                range: [0, Math.max(...yData) * 1.1] 
            }, horizontalGrid, verticalGrid), true);
            break;
            
        case 'pie':
            const pieValues = yColumn ? yData : xData.map(() => 1);
            plotData = [{
                type: 'pie',
                labels: xData,
                values: pieValues,
                textinfo: 'label+percent',
                textposition: 'auto',
                marker: {
                    colors: generatePlotlyColors(xData.length)
                },
                name: 'Distribution'
            }];
            break;
            
        case 'histogram':
            plotData = [{
                type: 'histogram',
                x: xData,
                nbinsx: 30,
                marker: { color: '#e94560', opacity: 0.7 },
                name: 'Frequency'
            }];
            
            layout.xaxis = applyGridSettings({ 
                title: xAxisTitle || xColumn, 
                gridcolor: 'rgba(255,255,255,0.1)', 
                color: 'white',
                range: [Math.min(...xData), Math.max(...xData)]
            }, verticalGrid, horizontalGrid);
            
            layout.yaxis = applyPrefixSuffix(applyGridSettings({ 
                title: 'Frequency', 
                gridcolor: 'rgba(255,255,255,0.1)', 
                color: 'white', 
                zeroline: true, 
                zerolinecolor: 'gray', 
                zerolinewidth: 2 
            }, horizontalGrid, verticalGrid), true);
            break;
            
        case 'box':
            plotData = [{
                type: 'box',
                y: yData,
                name: yColumn || 'Values',
                marker: { color: '#e94560' },
                boxpoints: 'outliers'
            }];
            
            layout.yaxis = applyPrefixSuffix(applyGridSettings({ 
                title: yAxisTitle || yColumn || 'Value', 
                gridcolor: 'rgba(255,255,255,0.1)', 
                color: 'white', 
                zeroline: true, 
                zerolinecolor: 'gray', 
                zerolinewidth: 2 
            }, horizontalGrid, verticalGrid), true);
            break;
            
        case 'heatmap':
            const uniqueX = [...new Set(xData)];
            const uniqueY = [...new Set(yData)];
            
            const zMatrix = Array(uniqueY.length).fill().map(() => Array(uniqueX.length).fill(0));
            
            data.forEach(row => {
                const xIdx = uniqueX.indexOf(row[xColumn]);
                const yIdx = uniqueY.indexOf(row[yColumn]);
                if (xIdx !== -1 && yIdx !== -1) {
                    zMatrix[yIdx][xIdx] += 1;
                }
            });
            
            plotData = [{
                type: 'heatmap',
                z: zMatrix,
                x: uniqueX,
                y: uniqueY,
                colorscale: 'Viridis',
                showscale: true,
                name: 'Heatmap'
            }];
            
            layout.xaxis = applyGridSettings({ 
                title: xAxisTitle || xColumn, 
                color: 'white',
                range: [-0.5, uniqueX.length - 0.5]
            }, verticalGrid, horizontalGrid);
            
            layout.yaxis = applyGridSettings({ 
                title: yAxisTitle || yColumn, 
                color: 'white', 
                zeroline: true, 
                zerolinecolor: 'gray', 
                zerolinewidth: 2 
            }, horizontalGrid, verticalGrid);
            break;
    }
    
    // Add footnote and source annotations if provided (keep existing code)
    if (footnote && footnote.trim()) {
        if (!layout.annotations) {
            layout.annotations = [];
        }
        
        layout.annotations.push({
            text: `<i>${wrapFootnoteText(footnote)}</i>`,
            xref: 'paper',
            yref: 'paper',
            x: 0,
            y: -0.15,
            xanchor: 'left',
            yanchor: 'top',
            width: 0.3,
            align: 'left',
            font: {
                size: 12,
                color: 'rgba(255,255,255,0.8)',
                family: 'Arial, sans-serif'
            },
            bgcolor: 'rgba(0,0,0,0)',
            bordercolor: 'rgba(0,0,0,0)',
            borderwidth: 0,
            showarrow: false
        });
    }
    
    if (source && source.trim()) {
        if (!layout.annotations) {
            layout.annotations = [];
        }
        
        layout.annotations.push({
            text: wrapSourceText(source),
            xref: 'paper',
            yref: 'paper',
            x: 1,
            y: -0.15,
            xanchor: 'right',
            yanchor: 'top',
            width: 0.3,
            align: 'right',
            font: {
                size: 12,
                color: 'rgba(255,255,255,0.8)',
                family: 'Arial, sans-serif'
            },
            bgcolor: 'rgba(0,0,0,0)',
            bordercolor: 'rgba(0,0,0,0)',
            borderwidth: 0,
            showarrow: false
        });
    }
    
    return { data: plotData, layout, config };
}

// ADD: Event listener to enable/disable radio buttons based on prefix/suffix fields
document.addEventListener('DOMContentLoaded', function() {
    const yPrefixField = document.getElementById('yPrefix');
    const ySuffixField = document.getElementById('ySuffix');
    const radioGroup = document.querySelector('.radio-group');
    
    function updateRadioState() {
        const hasValue = (yPrefixField && yPrefixField.value) || (ySuffixField && ySuffixField.value);
        
        if (radioGroup) {
            if (hasValue) {
                radioGroup.classList.remove('disabled');
                radioGroup.querySelectorAll('input[type="radio"]').forEach(radio => {
                    radio.disabled = false;
                });
            } else {
                radioGroup.classList.add('disabled');
                radioGroup.querySelectorAll('input[type="radio"]').forEach(radio => {
                    radio.disabled = true;
                });
            }
        }
    }
    
    // Add listeners
    if (yPrefixField) {
        yPrefixField.addEventListener('input', updateRadioState);
    }
    if (ySuffixField) {
        ySuffixField.addEventListener('input', updateRadioState);
    }
    
    // Initial state
    updateRadioState();
});

// ADD: Real-time update when prefix/suffix or radio changes (optional enhancement)
['yPrefix', 'ySuffix'].forEach(id => {
    const element = document.getElementById(id);
    if (element) {
        element.addEventListener('change', () => {
            if (currentData.length > 0 && currentChart) {
                // Could trigger chart regeneration here if desired
                // generateChart();
            }
        });
    }
});

document.querySelectorAll('input[name="prefixSuffixTopOnly"]').forEach(radio => {
    radio.addEventListener('change', () => {
        if (currentData.length > 0 && currentChart) {
            // Could trigger chart regeneration here if desired
            // generateChart();
        }
    });
});
</script>