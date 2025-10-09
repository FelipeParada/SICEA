import React, { useState } from "react";
import NavBar from "./NavBar";
import { Download, Droplets, Zap } from "lucide-react";
import axios from "axios";

const ExportPage: React.FC = () => {
  const [meterType, setMeterType] = useState<"WATER" | "ELECTRICITY" | "">("");

  const months = [
    { value: "01", label: "Enero" },
    { value: "02", label: "Febrero" },
    { value: "03", label: "Marzo" },
    { value: "04", label: "Abril" },
    { value: "05", label: "Mayo" },
    { value: "06", label: "Junio" },
    { value: "07", label: "Julio" },
    { value: "08", label: "Agosto" },
    { value: "09", label: "Septiembre" },
    { value: "10", label: "Octubre" },
    { value: "11", label: "Noviembre" },
    { value: "12", label: "Diciembre" },
  ];

  const currentYear = new Date().getFullYear();
  const [startMonth, setStartMonth] = useState("01");
  const [startYear, setStartYear] = useState(currentYear.toString());
  const [endMonth, setEndMonth] = useState("01");
  const [endYear, setEndYear] = useState(currentYear.toString());

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!meterType || !startMonth || !startYear || !endMonth || !endYear) {
      setError("Por favor, completa todos los campos.");
      return;
    }

    const startDate = `${startYear}-${startMonth}`;
    const endDate = `${endYear}-${endMonth}`;

    setLoading(true);
    try {
      const params = { meter_type: meterType, start_date: startDate, end_date: endDate };

      const response = await axios.get("http://localhost:8000/api/writer/export-excel/", {
        params,
        responseType: "arraybuffer",
      });

      const blob = new Blob([response.data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;

      let company = "";
      if (meterType === "WATER") company = "AguasAndinas";
      else if (meterType === "ELECTRICITY") company = "Enel";

      link.download = `Facturas_${company}_${startDate}_a_${endDate}.xlsx`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Error desconocido al exportar.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <NavBar />
      <div className="pt-20 min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex flex-col items-center justify-center px-4">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-10 w-full max-w-xl border border-white/20">
          <h1 className="text-3xl font-bold text-white text-center mb-6">Exportar Información</h1>

          {error && (
            <div className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200 text-sm text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Tipo de medidor */}
            <div>
              <label className="block text-blue-100 mb-2 font-medium">Tipo de Medidor</label>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setMeterType("WATER")}
                  className={`flex items-center justify-center gap-2 w-1/2 py-3 rounded-lg font-semibold transition-all duration-200 ${
                    meterType === "WATER"
                      ? "bg-blue-600 text-white shadow-lg"
                      : "bg-white/10 text-blue-200 hover:bg-white/20"
                  }`}
                >
                  <Droplets className="w-5 h-5" />
                  Agua
                </button>
                <button
                  type="button"
                  onClick={() => setMeterType("ELECTRICITY")}
                  className={`flex items-center justify-center gap-2 w-1/2 py-3 rounded-lg font-semibold transition-all duration-200 ${
                    meterType === "ELECTRICITY"
                      ? "bg-yellow-500 text-white shadow-lg"
                      : "bg-white/10 text-blue-200 hover:bg-white/20"
                  }`}
                >
                  <Zap className="w-5 h-5" />
                  Electricidad
                </button>
              </div>
            </div>

            {/* Selección de mes y año */}
            <div className="grid grid-cols-2 gap-6">
              {/* Fecha de inicio */}
              <div>
                <label className="block text-blue-100 mb-2 font-medium">Fecha de Inicio</label>
                <div className="flex gap-2">
                  <select
                    value={startMonth}
                    onChange={(e) => setStartMonth(e.target.value)}
                    className="w-1/2 bg-slate-800 text-white py-2 px-3 rounded-lg border border-white/30"
                  >
                    {months.map((m) => (
                      <option key={m.value} value={m.value}>{m.label}</option>
                    ))}
                  </select>
                  <input
                    type="number"
                    min={2000}
                    max={currentYear}
                    value={startYear}
                    onChange={(e) => setStartYear(e.target.value)}
                    className="w-1/2 bg-slate-800 text-white py-2 px-3 rounded-lg border border-white/30"
                  />
                </div>
              </div>

              {/* Fecha de fin */}
              <div>
                <label className="block text-blue-100 mb-2 font-medium">Fecha de Fin</label>
                <div className="flex gap-2">
                  <select
                    value={endMonth}
                    onChange={(e) => setEndMonth(e.target.value)}
                    className="w-1/2 bg-slate-800 text-white py-2 px-3 rounded-lg border border-white/30"
                  >
                    {months.map((m) => (
                      <option key={m.value} value={m.value}>{m.label}</option>
                    ))}
                  </select>
                  <input
                    type="number"
                    min={2000}
                    max={currentYear}
                    value={endYear}
                    onChange={(e) => setEndYear(e.target.value)}
                    className="w-1/2 bg-slate-800 text-white py-2 px-3 rounded-lg border border-white/30"
                  />
                </div>
              </div>
            </div>

            {/* Botón de exportar */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 text-white font-semibold py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all duration-200 hover:scale-[1.02]"
            >
              {loading ? (
                <>
                  <Download className="w-5 h-5 animate-bounce" />
                  Generando Excel...
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  Exportar Excel
                </>
              )}
            </button>
          </form>
        </div>

        <div className="text-center mt-12">
          <p className="text-blue-200/60 text-sm">© 2025 SICEA. Todos los derechos reservados.</p>
        </div>
      </div>
    </div>
  );
};

export default ExportPage;
