'use client'

import { useState, FormEvent } from 'react'

export default function Home() {
  const [input, setInput] = useState<string>('')
  const [response, setResponse] = useState<string>('')

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      })

      if (!res.ok) {
        throw new Error('Network response was not ok')
      }

      const data: { response: string } = await res.json()
      setResponse(data.response)
    } catch (error) {
      console.error('Fetch error:', error)
      setResponse('Something went wrong.')
    }
  }

  return (
    <main className="max-w-2xl mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold mb-6">Ask Virtual You</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me something..."
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Ask
        </button>
      </form>
      {response && (
        <div className="mt-6 p-4 border rounded bg-gray-50">
          <strong>Response:</strong>
          <p>{response}</p>
        </div>
      )}
    </main>
  )
}
