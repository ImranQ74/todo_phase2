"use client"

import { useState, useEffect, useCallback } from 'react'

interface UseVoiceOptions {
  onCommand?: (command: string) => void
  lang?: string
}

export function useVoice({ onCommand, lang = 'en-US' }: UseVoiceOptions = {}) {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [isSupported, setIsSupported] = useState(false)
  const [recognition, setRecognition] = useState<any>(null)

  useEffect(() => {
    if (typeof window !== 'undefined' && (window as any).webkitSpeechRecognition) {
      setIsSupported(true)
      const recognitionInstance = new (window as any).webkitSpeechRecognition()
      recognitionInstance.continuous = false
      recognitionInstance.interimResults = false
      recognitionInstance.lang = lang

      recognitionInstance.onstart = () => setIsListening(true)
      recognitionInstance.onend = () => setIsListening(false)

      recognitionInstance.onresult = (event: any) => {
        const current = event.resultIndex
        const transcriptText = event.results[current][0].transcript
        setTranscript(transcriptText)
        if (onCommand) {
          onCommand(transcriptText)
        }
      }

      setRecognition(recognitionInstance)
    }
  }, [lang, onCommand])

  const startListening = useCallback(() => {
    if (recognition && !isListening) {
      try {
        recognition.start()
      } catch (e) {
        console.error("Speech recognition already started")
      }
    }
  }, [recognition, isListening])

  const stopListening = useCallback(() => {
    if (recognition && isListening) {
      recognition.stop()
    }
  }, [recognition, isListening])

  return {
    isListening,
    transcript,
    isSupported,
    startListening,
    stopListening
  }
}
