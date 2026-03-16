export interface ContextualMeaningResponse {
  word: string;
  definition?: string | null;
  confidence: number;
  sense_id?: string | null;
}
