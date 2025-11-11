document.addEventListener('alpine:init', () => {
    Alpine.data('adherenceApp', () => ({
        // --- State ---
        age: 45,
        gender: 'Male',
        period: 3,
        smsReminder: true,

        riskFactors: [
            { label: 'Diabetes', key: 'diabetes', model: true, weight: 1.8 },
            { label: 'Hypertension', key: 'hypertension', model: true, weight: 1.5 },
            { label: 'Alcoholism', key: 'alcoholism', model: false, weight: 2.5 },
            { label: 'Smokes', key: 'smokes', model: false, weight: 1.2 },
            { label: 'Tuberculosis', key: 'tuberculosis', model: false, weight: 3.0 },
        ],

        isAdhering: null,
        showResult: false,
        confidence: 0,
        iod: 88,
        f1: 85,

        init() {
            this.predictAdherence();
            this.$nextTick(() => this.initChart());
        },

        // --- Methods ---
        scrollToForm() {
            document.getElementById('form').scrollIntoView({ behavior: 'smooth' });
        },

        predictAdherence() {
            // Calculate risk score
            let riskScore = 0;
            this.riskFactors.forEach(f => { if(f.model) riskScore += f.weight; });
            if(this.age < 25 || this.age > 70) riskScore += 1.0;
            if(this.period > 12) riskScore += 1.5;
            if(this.smsReminder) riskScore -= 3.0;

            const maxRisk = 12.5;
            let baseConfidence = 100 - (riskScore / maxRisk) * 100;

            // Add small input-based variation
            let activeFactors = this.riskFactors.filter(f => f.model).length;
            let variation = activeFactors * 0.5;
            this.confidence = Math.max(0, Math.min(100, baseConfidence + (Math.random() * variation - variation / 2)));

            // Determine adherence
            this.isAdhering = this.confidence >= 60;

            // Update model metrics slightly based on risk
            this.iod = Math.max(70, 88 - activeFactors);       // IoD drops a bit with more risk
            this.f1 = Math.max(70, 85 - activeFactors * 0.5);  // F1 drops slightly

            // Show results
            this.showResult = true;

            // Update chart
            this.updateChart();
        },

        initChart() {
            const ctx = document.getElementById('riskChart').getContext('2d');
            if(window.riskChartInstance) window.riskChartInstance.destroy();

            window.riskChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: this.riskFactors.map(f => f.label),
                    datasets: [{
                        label: 'Risk Contribution',
                        data: this.riskFactors.map(f => f.model ? f.weight : f.weight * 0.3),
                        backgroundColor: ['#3b82f6','#06b6d4','#ef4444','#facc15','#a855f7'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, max: 4, ticks: { stepSize: 1 }, grid: { color: '#e5e7eb' } },
                        x: { grid: { display: false } }
                    }
                }
            });
        },
        

        updateChart() {
            if(window.riskChartInstance) {
                window.riskChartInstance.data.datasets[0].data =
                    this.riskFactors.map(f => f.model ? f.weight : f.weight * 0.3);
                window.riskChartInstance.update();
            }
        }
    }));
});
