// Better Auth configuration and client
import { betterAuth } from 'better-auth'
import { jwt } from 'better-auth/plugins'

// Server-side auth configuration
export const auth = betterAuth({
  database: {
    provider: 'postgresql',
    url: process.env.DATABASE_URL!,
  },
  plugins: [
    jwt({
      issuer: 'todo-app',
      expiration: 7 * 24 * 60 * 60, // 7 days in seconds
    }),
  ],
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
})

// Client-side auth client
import { createAuthClient } from 'better-auth/react'

export const authClient = createAuthClient({
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
})

export type Session = typeof authClient.$Infer.Session
export type User = typeof authClient.$Infer.User
