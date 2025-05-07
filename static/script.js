async function loadWorkdays() {
    try {
        const response = await fetch('/get_workdays');
        if (!response.ok) throw new Error('Failed to load workdays');
        const workdays = await response.json();
        const tbody = document.querySelector('#workdaysTable tbody');
        tbody.innerHTML = '';

        workdays.forEach((day, index) => {
            const row = document.createElement('tr');
            row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50';
            row.innerHTML = `
                <td class="border px-4 py-2">${day.date}</td>
                <td class="border px-4 py-2">${day.day_of_week}</td>
                <td class="border px-4 py-2">${day.is_workday}</td>
                ${Object.keys(day.agents).map(agent => `
                    <td class="border px-4 py-2 text-center">
                        <input type="checkbox" 
                               ${day.agents[agent] ? 'checked' : ''} 
                               onchange="updateWorkday('${day.date}', '${agent}', this.checked)"
                               ${day.is_workday === 'N' ? 'disabled' : ''}>
                    </td>
                `).join('')}
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading workdays:', error);
        alert('Failed to load workdays. Please try again.');
    }
}

async function updateWorkday(date, agent, missed) {
    try {
        const response = await fetch('/update_workday', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date, agent, missed })
        });
        if (!response.ok) throw new Error('Failed to update workday');
    } catch (error) {
        console.error('Error updating workday:', error);
        alert('Failed to update workday. Please try again.');
    }
}

async function calculateWages() {
    try {
        const response = await fetch('/calculate_wages');
        if (!response.ok) throw new Error('Failed to calculate wages');
        const monthlyWages = await response.json();
        const tbody = document.querySelector('#summaryTable tbody');
        tbody.innerHTML = '';

        monthlyWages.forEach((monthData, index) => {
            const row = document.createElement('tr');
            row.className = index % 2 === 0 ? 'bg-white' : 'bg-gray-50';
            row.innerHTML = `
                <td class="border px-4 py-2">${monthData.month}</td>
                ${Object.keys(monthData.wages).map(agent => `
                    <td class="border px-4 py-2">${monthData.wages[agent]}</td>
                `).join('')}
                <td class="border px-4 py-2 font-bold">${monthData.total_wage}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error calculating wages:', error);
        alert('Failed to calculate wages. Please try again.');
    }
}
