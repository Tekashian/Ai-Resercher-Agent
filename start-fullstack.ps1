# AI Research Agent - Start Script
# Starts both backend and frontend servers

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AI Research Agent - Full Stack Startup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend dependencies are installed
Write-Host "[1/4] Checking backend..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    Write-Host "  ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "  Please run: python -m venv .venv" -ForegroundColor Red
    exit 1
}
Write-Host "  Backend ready" -ForegroundColor Green

# Check if frontend dependencies are installed
Write-Host "[2/4] Checking frontend..." -ForegroundColor Yellow
if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "  Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location frontend
    npm install --legacy-peer-deps
    Set-Location ..
}
Write-Host "  Frontend ready" -ForegroundColor Green

# Start backend in background
Write-Host "[3/4] Starting backend server..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & .\.venv\Scripts\python.exe start.py
}
Write-Host "  Backend starting on http://localhost:8000" -ForegroundColor Green

# Wait a bit for backend to initialize
Start-Sleep -Seconds 3

# Start frontend in background
Write-Host "[4/4] Starting frontend server..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "$using:PWD\frontend"
    npm start
}
Write-Host "  Frontend starting on http://localhost:3000" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Servers are starting!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "  Press Ctrl+C to stop both servers" -ForegroundColor Yellow
Write-Host ""

# Keep script running and show logs
try {
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Check if jobs are still running
        if ($backendJob.State -ne 'Running') {
            Write-Host "Backend stopped!" -ForegroundColor Red
            break
        }
        if ($frontendJob.State -ne 'Running') {
            Write-Host "Frontend stopped!" -ForegroundColor Red
            break
        }
    }
}
finally {
    Write-Host ""
    Write-Host "Stopping servers..." -ForegroundColor Yellow
    Stop-Job $backendJob, $frontendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob, $frontendJob -ErrorAction SilentlyContinue
    Write-Host "Servers stopped." -ForegroundColor Green
}
