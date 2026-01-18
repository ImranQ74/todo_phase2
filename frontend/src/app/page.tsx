import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-blue-600">Todo App</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/signin"
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                Sign In
              </Link>
              <Link
                href="/signup"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 font-medium"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900">
            Manage Your Tasks
            <span className="block text-blue-600">Effortlessly</span>
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            A modern, full-stack todo application with authentication,
            persistent storage, and real-time synchronization. Built with
            Next.js, FastAPI, and Neon PostgreSQL.
          </p>
          <div className="mt-10 flex justify-center space-x-4">
            <Link
              href="/signup"
              className="bg-blue-600 text-white px-8 py-3 rounded-md text-lg font-medium hover:bg-blue-700"
            >
              Get Started Free
            </Link>
            <Link
              href="/signin"
              className="bg-white text-blue-600 px-8 py-3 rounded-md text-lg font-medium border border-blue-600 hover:bg-blue-50"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="mt-32">
          <h2 className="text-3xl font-bold text-center text-gray-900">
            Features
          </h2>
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-3xl mb-4">✓</div>
              <h3 className="text-xl font-semibold mb-2">JWT Authentication</h3>
              <p className="text-gray-600">
                Secure user authentication with JWT tokens and Better Auth
                integration.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-3xl mb-4">🗄️</div>
              <h3 className="text-xl font-semibold mb-2">Persistent Storage</h3>
              <p className="text-gray-600">
                Neon Serverless PostgreSQL ensures your tasks are always saved
                and accessible.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-3xl mb-4">📱</div>
              <h3 className="text-xl font-semibold mb-2">Responsive Design</h3>
              <p className="text-gray-600">
                Works seamlessly on desktop, tablet, and mobile devices with
                Tailwind CSS.
              </p>
            </div>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mt-32 mb-20">
          <h2 className="text-3xl font-bold text-center text-gray-900">
            Built With Modern Technologies
          </h2>
          <div className="mt-12 flex flex-wrap justify-center gap-8">
            <div className="bg-white px-6 py-4 rounded-lg shadow-md">
              <span className="text-blue-600 font-semibold">Next.js 14</span>
            </div>
            <div className="bg-white px-6 py-4 rounded-lg shadow-md">
              <span className="text-blue-600 font-semibold">FastAPI</span>
            </div>
            <div className="bg-white px-6 py-4 rounded-lg shadow-md">
              <span className="text-blue-600 font-semibold">Neon PostgreSQL</span>
            </div>
            <div className="bg-white px-6 py-4 rounded-lg shadow-md">
              <span className="text-blue-600 font-semibold">Better Auth</span>
            </div>
            <div className="bg-white px-6 py-4 rounded-lg shadow-md">
              <span className="text-blue-600 font-semibold">Tailwind CSS</span>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-500">
            <p>© 2025 Todo App - Phase 2: The Evolution of Todo</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
