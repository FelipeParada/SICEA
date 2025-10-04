import { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFiles(Array.from(event.target.files || []));
    setSuccess(null);
    setError(null);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setUploading(true);
    setSuccess(null);
    setError(null);

    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const token = localStorage.getItem('auth_token'); // <-- clave correcta
      await axios.post(
        'http://localhost:8000/api/reader/process-multiple-bills/',
        formData,
        {
          headers: {
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setSuccess('Archivos subidos correctamente.');
      setFiles([]);
      const input = document.getElementById('file-input') as HTMLInputElement;
      if (input) input.value = '';
    } catch (err: any) {
      setError('Error al subir archivos');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex items-center justify-center p-4">
      <div className="w-full max-w-lg">
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-white/20">
          <h1 className="text-3xl font-bold text-white mb-6 text-center">Subir Boletas</h1>
          {success && (
            <div className="mb-4 p-3 bg-green-500/20 border border-green-500/30 rounded-lg text-green-200 text-center text-sm">
              {success}
            </div>
          )}
          {error && (
            <div className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200 text-center text-sm">
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-6">
            <input
              id="file-input"
              type="file"
              multiple
              accept=".pdf"
              onChange={handleFileSelect}
              className="block w-full text-white bg-white/10 border border-white/30 rounded-lg px-4 py-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all duration-200 hover:bg-white/15"
            />
            <button
              type="submit"
              disabled={uploading || files.length === 0}
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-blue-400 disabled:to-blue-500 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:hover:scale-100 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-transparent shadow-lg hover:shadow-xl flex items-center justify-center"
            >
              {uploading ? 'Subiendo...' : `Guardar ${files.length} archivo${files.length !== 1 ? 's' : ''}`}
            </button>
          </form>
          {files.length > 0 && (
            <div className="mt-6">
              <p className="text-blue-200 mb-2">Archivos seleccionados:</p>
              <ul className="list-disc list-inside text-white text-sm">
                {files.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
        <div className="text-center mt-8">
          <p className="text-blue-200/60 text-sm">
            © 2025 SICEA. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;