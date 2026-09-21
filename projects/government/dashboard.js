let dashboardData = null;

        async function loadData() {
            try {
                const response = await fetch('dashboard_data.json');
                dashboardData = await response.json();

                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboardContent').removeAttribute('hidden');

                populateMetrics();
                populateRiskTable();
                initCharts();
                setupSidebarNavigation();
                
            } catch (error) {
                document.getElementById('loading').innerHTML = `
                    <div class="loading-error"><h2>Unable to load service report</h2><p>The service report data could not be loaded.</p>
                    <p class="error-detail">${error.message}</p></div>
                `;
            }
        }

        function populateMetrics() {
            const metrics = dashboardData.metrics;
            const grid = document.getElementById('metricsGrid');

            const metricItems = [
                { icon: 'file-text', color: '#1f70bd', label: 'Requests received', value: metrics.total_requests.toLocaleString(), change: 'Reporting period: 2022 to 2025' },
                { icon: 'circle-check', color: '#239363', label: 'Completed', value: metrics.resolved_requests.toLocaleString(), change: 'Across all departments' },
                { icon: 'clock', color: '#e2a326', label: 'Still open', value: metrics.pending_requests.toLocaleString(), change: 'Awaiting completion' },
                { icon: 'timer', color: '#6949ad', label: 'Completed on time', value: metrics.sla_compliance_rate.toFixed(1) + '%', change: 'Target: 80%' },
                { icon: 'triangle-alert', color: '#d94444', label: 'Requests escalated', value: metrics.escalation_rate.toFixed(1) + '%', change: 'Cases requiring review' },
                { icon: 'gauge', color: '#477eaf', label: 'Average completion time', value: metrics.avg_resolution_days.toFixed(1) + ' days', change: 'All completed requests' }
            ];

            grid.innerHTML = metricItems.map(m => `
                <article class="metric-card" style="--metric-accent:${m.color}"><span class="metric-icon" aria-hidden="true"><i data-lucide="${m.icon}"></i></span><div class="metric-copy"><h3 class="metric-label">${m.label}</h3><div class="metric-value">${m.value}</div><span class="metric-support">${m.change}</span></div></article>
            `).join('');
            if (window.lucide) lucide.createIcons();
        }

        function populateRiskTable() {
            const tbody = document.querySelector('#riskTable tbody');
            const requests = dashboardData.high_risk;

            if (!requests || requests.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="empty-state">No pending requests currently require urgent attention.</td></tr>`;
                return;
            }

            tbody.innerHTML = requests.map(r => `
                <tr>
                    <td><strong>${r.request_id}</strong></td>
                    <td>${r.department}</td>
                    <td>${r.service_type}</td>
                    <td>${r.channel}</td>
                    <td>${r.submitted}</td>
                    <td>
                        <span class="badge ${r.risk_level === 'Critical' ? 'badge-critical' : r.risk_level === 'High' ? 'badge-high' : r.risk_level === 'Medium' ? 'badge-medium' : 'badge-low'}">
                            ${r.risk_level}
                        </span>
                    </td>
                    <td>${(r.escalation_probability * 100).toFixed(0)}%</td>
                </tr>
            `).join('');
        }

        function initCharts() {
            const departments = dashboardData.departments;
            const channels = dashboardData.channels;
            const services = dashboardData.services;
            const escalations = dashboardData.escalations;
            const monthly = dashboardData.monthly;

            // Department Chart
            const deptNames = Object.keys(departments);
            const deptSLA = deptNames.map(d => departments[d].sla_rate);
            const deptColors = deptSLA.map(s => s >= 80 ? '#25865d' : s >= 50 ? '#d89a31' : '#c14f45');

            new Chart(document.getElementById('deptChart'), {
                type: 'bar',
                data: {
                    labels: deptNames,
                    datasets: [{
                        label: 'Completed on time (%)',
                        data: deptSLA,
                        backgroundColor: deptColors,
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'end',
                            formatter: (v) => v.toFixed(1) + '%'
                        }
                    },
                    scales: {
                        y: { beginAtZero: true, max: 100, ticks: { callback: (v) => v + '%' } }
                    }
                },
                plugins: [ChartDataLabels]
            });

            // Department Escalation Chart
            const deptEsc = deptNames.map(d => departments[d].escalation_rate);

            new Chart(document.getElementById('deptEscalationChart'), {
                type: 'bar',
                data: {
                    labels: deptNames,
                    datasets: [{
                        label: 'Requests escalated (%)',
                        data: deptEsc,
                        backgroundColor: deptEsc.map(e => e > 20 ? '#c14f45' : e > 10 ? '#d89a31' : '#25865d'),
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'end',
                            formatter: (v) => v.toFixed(1) + '%'
                        }
                    },
                    scales: {
                        y: { beginAtZero: true, ticks: { callback: (v) => v + '%' } }
                    }
                },
                plugins: [ChartDataLabels]
            });

            // Channel Chart
            const channelNames = Object.keys(channels);
            const channelSLA = channelNames.map(c => channels[c].sla_rate);

            new Chart(document.getElementById('channelChart'), {
                type: 'bar',
                data: {
                    labels: channelNames,
                    datasets: [{
                        label: 'Completed on time (%)',
                        data: channelSLA,
                        backgroundColor: channelSLA.map(s => s >= 80 ? '#25865d' : s >= 50 ? '#d89a31' : '#c14f45'),
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'end',
                            formatter: (v) => v.toFixed(1) + '%'
                        }
                    },
                    scales: {
                        y: { beginAtZero: true, max: 100, ticks: { callback: (v) => v + '%' } }
                    }
                },
                plugins: [ChartDataLabels]
            });

            // Channel Time Chart
            const channelTimes = channelNames.map(c => channels[c].actual_days);

            new Chart(document.getElementById('channelTimeChart'), {
                type: 'bar',
                data: {
                    labels: channelNames,
                    datasets: [{
                        label: 'Average completion (days)',
                        data: channelTimes,
                        backgroundColor: ['#236bb0','#397cb9','#4d8bc0','#6d78ad'],
                        borderRadius: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'end',
                            formatter: (v) => v.toFixed(1) + ' days'
                        }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                },
                plugins: [ChartDataLabels]
            });

            // Escalation Chart
            const escNames = Object.keys(escalations);
            const escCounts = escNames.map(e => escalations[e].request_id);

            new Chart(document.getElementById('escalationChart'), {
                type: 'bar',
                data: {
                    labels: escNames,
                    datasets: [{
                        label: 'Escalated requests',
                        data: escCounts,
                        backgroundColor: deptEsc.map((e,i) => i === 0 ? '#c84f4a' : i < 3 ? '#dfa62d' : '#4d88a8'),
                        borderRadius: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: {
                            anchor: 'end',
                            align: 'end',
                            formatter: (v) => v
                        }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                },
                plugins: [ChartDataLabels]
            });

            // Service Chart
            const servicePairs = Object.keys(services).map(name => ({ name, missed: 100 - services[name].sla_rate })).sort((a, b) => b.missed - a.missed);
            const serviceNames = servicePairs.map(item => item.name);
            const serviceEsc = servicePairs.map(item => item.missed);

            new Chart(document.getElementById('serviceChart'), {
                type: 'bar',
                data: {
                    labels: serviceNames,
                    datasets: [{
                        label: 'Requests escalated (%)',
                        data: serviceEsc,
                        backgroundColor: serviceEsc.map(e => e > 20 ? '#c14f45' : e > 10 ? '#d89a31' : '#25865d'),
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false, indexAxis: 'y',
                    plugins: { legend: { display: false }, datalabels: { anchor: 'end', align: 'right', formatter: (v) => v.toFixed(1) + '%' } },
                    scales: { x: { beginAtZero: true, max: 100, ticks: { callback: (v) => v + '%' } }, y: { grid: { display: false } } }
                },
                plugins: [ChartDataLabels]
            });

            // Trend Chart
            const monthLabels = Object.keys(monthly);
            const monthCounts = monthLabels.map(m => monthly[m].request_id);
            const monthSLA = monthLabels.map(m => monthly[m].sla_rate);

            new Chart(document.getElementById('monthlyChart'), {
                type: 'line',
                data: {
                    labels: monthLabels,
                    datasets: [
                        {
                            label: 'Requests received',
                            data: monthCounts,
                            borderColor: '#3e75a3',
                            backgroundColor: 'rgba(62,117,163,.10)',
                            fill: true,
                            tension: 0.4,
                            yAxisID: 'y'
                        },
                        {
                            label: 'Completed on time %',
                            data: monthSLA,
                            borderColor: '#25865d',
                            backgroundColor: 'rgba(37,134,93,.08)',
                            fill: true,
                            tension: 0.4,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { position: 'top' },
                        datalabels: { display: false }
                    },
                    scales: {
                        y: { beginAtZero: true, position: 'left' },
                        y1: { beginAtZero: true, position: 'right', max: 100, grid: { drawOnChartArea: false } }
                    }
                },
                plugins: [ChartDataLabels]
            });
        }

        function setupSidebarNavigation() {
            const links = document.querySelectorAll('.sidebar-nav a');
            const sections = document.querySelectorAll('.section');

            links.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();

                    links.forEach(l => l.classList.remove('active'));
                    this.classList.add('active');

                    const targetId = this.getAttribute('href');
                    const targetSection = document.querySelector(targetId);
                    if (targetSection) {
                        targetSection.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            });

            window.addEventListener('scroll', function() {
                let current = '';
                sections.forEach(section => {
                    const sectionTop = section.offsetTop - 100;
                    if (window.scrollY >= sectionTop) {
                        current = section.getAttribute('id');
                    }
                });

                links.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + current) {
                        link.classList.add('active');
                    }
                });
            });
        }

        // Load data on page load
        loadData();
