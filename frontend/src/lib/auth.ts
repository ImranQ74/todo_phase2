// Better Auth configuration and client
import { betterAuth } from 'better-auth'

// Server-side auth configuration
export const auth = process.env.DATABASE_URL ? betterAuth({
  database: {
    provider: 'postgresql',
    url: process.env.DATABASE_URL,
  },
  // plugins: [
  //   jwt({
  //     issuer: 'todo-app',
  //     expiration: 7 * 24 * 60 * 60, // 7 days in seconds
  //   }),
  // ],
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
}) :  betterAuth({
    database: {
        provider: "sqlite",
        url: ":memory:"
    }
})

// Server-side auth configuration
