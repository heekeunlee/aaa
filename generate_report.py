
import csv
import json
import random

# Generate multi-batch data to allow for animation like the reference image
batches = ["Step 01", "Step 02", "Step 03", "Step 04", "Step 05"]
data = []
for batch in batches:
    # Simulate process evolution or variation across steps
    batch_mean = 1.5 + (batches.index(batch) * 0.005) # Slight shift
    for _ in range(200):
        data.append({
            'step': batch,
            'x': round(random.uniform(-100, 100), 2),
            'y': round(random.uniform(-100, 100), 2),
            'cd': round(random.normalvariate(batch_mean, 0.025), 4)
        })

data_json = json.dumps(data)

html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Semiconductor CD Advanced Analysis</title>
    <!-- Use Plotly.js for premium interactive visualizations as requested -->
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js"></script>
    <style>
        body { font-family: 'Inter', system-ui, -apple-system, sans-serif; margin: 0; background: #fdfdfd; color: #1e293b; overflow-x: hidden; }
        
        #splash-screen { position: fixed; inset: 0; background: #0f172a; z-index: 9999; display: flex; align-items: center; justify-content: center; transition: opacity 0.8s ease; }
        .splash-content { text-align: center; color: white; }
        .splash-logo { font-size: 32px; font-weight: 800; letter-spacing: -1px; margin-bottom: 20px; background: linear-gradient(135deg, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .loading-bar-bg { width: 240px; height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px; margin: auto; overflow: hidden; }
        .loading-bar-fill { width: 0%; height: 100%; background: #60a5fa; transition: width 3s linear; box-shadow: 0 0 15px rgba(96, 165, 250, 0.5); }

        .report-main { max-width: 1200px; margin: 40px auto; padding: 0 20px; display: none; opacity: 0; transition: opacity 1s ease; }
        header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; border-bottom: 1px solid #e2e8f0; padding-bottom: 20px; }
        h1 { margin: 0; font-size: 28px; font-weight: 800; color: #0f172a; }
        .subtitle { color: #64748b; margin-top: 5px; font-size: 15px; }

        .viz-card { background: white; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 40px; }
        .viz-title { font-size: 18px; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        .viz-title span { width: 4px; height: 18px; background: #6366f1; border-radius: 2px; }

        .btn-group { display: flex; gap: 12px; }
        .btn-action { padding: 10px 18px; border-radius: 10px; border: none; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s; font-size: 14px; }
        .btn-pptx { background: #fef2f2; color: #dc2626; border: 1px solid #fee2e2; }
        .btn-pdf { background: #f8fafc; color: #0f172a; border: 1px solid #e2e8f0; }
        .btn-action:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); opacity: 0.9; }

        #chart-div { width: 100%; height: 650px; }
        
        .footer { text-align: center; color: #94a3b8; font-size: 13px; margin: 60px 0; }
        
        @media print { .btn-group, #splash-screen { display: none !important; } .report-main { display: block !important; opacity: 1 !important; margin: 0; padding: 0; } }
    </style>
</head>
<body>
    <div id="splash-screen">
        <div class="splash-content">
            <div class="splash-logo">VIBE CODING LECTURE</div>
            <div class="loading-bar-bg"><div class="loading-bar-fill" id="loading-bar"></div></div>
            <p style="margin-top: 20px; color: #94a3b8; font-size: 14px;">고급 인터랙티브 시각화 로딩 중...</p>
        </div>
    </div>

    <div class="report-main" id="root">
        <header>
            <div>
                <h1>반도체 공정 선폭(CD) 동적 분석 리포트</h1>
                <p class="subtitle">Time-series Wafer Mapping & Advanced Distribution Analysis</p>
            </div>
            <div class="btn-group">
                <button class="btn-action btn-pptx" onclick="exportToPPTX()">PPTX 내보내기</button>
                <button class="btn-action btn-pdf" onclick="window.print()">PDF 내보내기</button>
            </div>
        </header>

        <section class="viz-card">
            <div class="viz-title"><span></span>공정 단계별 선폭분포 시뮬레이션 (Bubble Chart Animation)</div>
            <div id="chart-div"></div>
        </section>

        <div class="footer">&copy; 2026 Vibe Coding Engineering Edu. Designed for Advanced Learning.</div>
    </div>

    <script>
        const rawData = {{DATA_JSON}};
        const steps = [...new Set(rawData.map(d => d.step))].sort();
        
        function initPlotly() {
            const frames = steps.map(step => {
                const stepData = rawData.filter(d => d.step === step);
                return {
                    name: step,
                    data: [{
                        x: stepData.map(d => d.x),
                        y: stepData.map(d => d.y),
                        text: stepData.map(d => `CD: ${d.cd}μm`),
                        mode: 'markers',
                        marker: {
                            size: stepData.map(d => (d.cd - 1.4) * 500), // Bubble size logic
                            color: stepData.map(d => d.cd),
                            colorscale: 'Viridis',
                            showscale: true,
                            colorbar: { title: 'CD (μm)', thickness: 15 },
                            opacity: 0.7,
                            line: { color: 'white', width: 0.5 }
                        }
                    }]
                };
            });

            const initialData = frames[0].data;

            const layout = {
                xaxis: { title: 'Wafer X-Pos (mm)', range: [-110, 110], gridcolor: '#f1f5f9' },
                yaxis: { title: 'Wafer Y-Pos (mm)', range: [-110, 110], gridcolor: '#f1f5f9' },
                hovermode: 'closest',
                plot_bgcolor: '#f8fafc',
                paper_bgcolor: 'white',
                margin: { t: 30, b: 80, l: 60, r: 10 },
                updatemenus: [{
                    x: 0, y: 0,
                    yanchor: 'top', xanchor: 'left',
                    showactive: false,
                    direction: 'left',
                    type: 'buttons',
                    pad: { t: 87, r: 10 },
                    buttons: [{
                        method: 'animate',
                        args: [null, {
                            fromcurrent: true,
                            transition: { duration: 500, easing: 'quadratic-in-out' },
                            frame: { duration: 1000, redraw: false }
                        }],
                        label: '▶ Play'
                    }, {
                        method: 'animate',
                        args: [[null], {
                            mode: 'immediate',
                            transition: { duration: 0 },
                            frame: { duration: 0, redraw: false }
                        }],
                        label: '❙❙ Pause'
                    }]
                }],
                sliders: [{
                    active: 0,
                    steps: steps.map(step => ({
                        label: step,
                        method: 'animate',
                        args: [[step], {
                            mode: 'immediate',
                            transition: { duration: 300 },
                            frame: { duration: 300, redraw: false }
                        }]
                    })),
                    x: 0.1, len: 0.9,
                    currentvalue: { visible: true, prefix: 'Step: ', xanchor: 'right', font: { size: 16, color: '#6366f1' } },
                    pad: { t: 50 }
                }]
            };

            Plotly.newPlot('chart-div', initialData, layout).then(() => {
                Plotly.addFrames('chart-div', frames);
            });
        }

        async function exportToPPTX() {
            const pptx = new PptxGenJS();
            const slide = pptx.addSlide();
            slide.addText("반도체 공정 선폭(CD) 분석 보고서", { x: 0.5, y: 0.5, fontSize: 24, bold: true, color: '0f172a' });
            
            // Capture current chart state
            const imgData = await Plotly.toImage('chart-div', { format: 'png', width: 900, height: 600 });
            slide.addImage({ data: imgData, x: 0.5, y: 1.2, w: 9, h: 5 });
            
            pptx.writeFile({ fileName: "CD_Analysis_Advanced_Report.pptx" });
        }

        window.onload = () => {
            const bar = document.getElementById('loading-bar');
            const splash = document.getElementById('splash-screen');
            const root = document.getElementById('root');
            
            setTimeout(() => { bar.style.width = '100%'; }, 100);
            
            setTimeout(() => {
                splash.style.opacity = '0';
                root.style.display = 'block';
                setTimeout(() => {
                    splash.style.display = 'none';
                    root.style.opacity = '1';
                    initPlotly();
                }, 800);
            }, 3000);
        };
    </script>
</body>
</html>
"""

final_html = html_template.replace('{{DATA_JSON}}', data_json)

with open('cd_analysis_report.html', 'w') as f:
    f.write(final_html)

with open('index.html', 'w') as f:
    f.write(final_html)

print("Advanced Plotly report generated with Gapminder-style animation.")
