 import { getTotalMetrics } from "@/app/lib/api"

 export default async function Dashboard() {
    
    const { totalFinished, totalWinning, totalDraw } = await getTotalMetrics();

    return (
        <div>
            <div>
                <h3>Total de Partidas</h3>
                { totalFinished}
            </div>
            <div>
                <h3>Total de Vitórias</h3>
                {}
            </div>
            <div>
                <h3>Total de Empates</h3>
                { totalDraw}
            </div>
        </div>
    )
 }