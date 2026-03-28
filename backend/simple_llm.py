"""
Improved rule-based LLM for generating answers from context.
Uses better sentence extraction and answer construction.
"""
import re
from typing import List, Tuple


class SimpleLLM:
    """
    An improved rule-based system that extracts and combines relevant sentences
    to create coherent answers from context.
    """
    
    def generate(self, prompt: str) -> str:
        """Generate an answer based on the prompt."""
        question = self._extract_question(prompt)
        context = self._extract_context(prompt)
        
        if not context:
            return "I don't have enough context to answer this question."
        
        # Find relevant sentences with scores
        relevant_sentences = self._find_relevant_sentences(question, context)
        
        if not relevant_sentences:
            return "Based on the provided context, I cannot find specific information to answer this question."
        
        # Construct a coherent answer
        answer = self._construct_answer(question, relevant_sentences)
        return answer
    
    def _extract_question(self, prompt: str) -> str:
        """Extract the question from the prompt."""
        match = re.search(r'Question:\s*(.+?)(?:\n|$)', prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_context(self, prompt: str) -> str:
        """Extract the context from the prompt."""
        match = re.search(r'Context:\s*(.+?)(?:Question:|$)', prompt, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""
    
    def _find_relevant_sentences(self, question: str, context: str) -> List[Tuple[float, str]]:
        """Find sentences in context that are relevant to the question."""
        keywords = self._extract_keywords(question)
        
        # Split context into sentences (improved splitting)
        sentences = re.split(r'(?<=[.!?])\s+', context)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        # Score each sentence
        scored_sentences = []
        for sentence in sentences:
            score = self._score_sentence(sentence, keywords, question)
            if score > 0:
                scored_sentences.append((score, sentence))
        
        # Sort by score and return top sentences
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        return scored_sentences[:5]  # Return top 5 sentences
    
    def _score_sentence(self, sentence: str, keywords: List[str], question: str) -> float:
        """Score a sentence based on relevance to the question."""
        score = 0.0
        sentence_lower = sentence.lower()
        
        # Keyword matching (weighted)
        for keyword in keywords:
            if keyword in sentence_lower:
                # Exact word match gets higher score
                if re.search(r'\b' + re.escape(keyword) + r'\b', sentence_lower):
                    score += 2.0
                else:
                    score += 1.0
        
        # Bonus for definition patterns
        if any(pattern in sentence_lower for pattern in [' is ', ' are ', ' refers to ', ' means ']):
            score += 1.5
        
        # Bonus for explanatory patterns
        if any(pattern in sentence_lower for pattern in ['because', 'therefore', 'thus', 'which', 'that']):
            score += 0.5
        
        # Penalty for very short sentences
        if len(sentence.split()) < 10:
            score *= 0.5
        
        # Bonus for longer, informative sentences
        if len(sentence.split()) > 20:
            score *= 1.2
        
        return score
    
    def _extract_keywords(self, question: str) -> List[str]:
        """Extract important keywords from the question."""
        stop_words = {
            'what', 'is', 'are', 'how', 'why', 'when', 'where', 'who', 'which',
            'the', 'a', 'an', 'to', 'do', 'does', 'can', 'should', 'would', 'could',
            'of', 'in', 'on', 'at', 'for', 'with', 'about', 'as', 'by', 'from',
            'this', 'that', 'these', 'those', 'i', 'you', 'we', 'they', 'it'
        }
        
        # Tokenize and filter
        words = re.findall(r'\b\w+\b', question.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def _construct_answer(self, question: str, scored_sentences: List[Tuple[float, str]]) -> str:
        """Construct a coherent answer from relevant sentences."""
        if not scored_sentences:
            return "I couldn't find relevant information in the context."
        
        sentences = [sent for score, sent in scored_sentences]
        
        # Check question type and construct appropriate answer
        question_lower = question.lower()
        
        # Definition questions
        if any(word in question_lower for word in ['what is', 'what are', 'define', 'definition of']):
            # Find the best definition sentence
            for sent in sentences:
                if any(pattern in sent.lower() for pattern in [' is ', ' are ', ' refers to ', ' means ']):
                    # Clean up the sentence
                    sent = self._clean_sentence(sent)
                    # Add context if needed
                    if len(sentences) > 1:
                        additional = self._clean_sentence(sentences[1])
                        return f"{sent} {additional}"
                    return sent
        
        # How-to questions
        if 'how to' in question_lower or 'how do' in question_lower or 'how can' in question_lower:
            answer_parts = []
            for sent in sentences[:3]:  # Use top 3 sentences
                cleaned = self._clean_sentence(sent)
                if cleaned and cleaned not in answer_parts:
                    answer_parts.append(cleaned)
            
            if len(answer_parts) == 1:
                return answer_parts[0]
            else:
                return " ".join(answer_parts)
        
        # Why questions
        if 'why' in question_lower:
            # Look for explanatory sentences
            for sent in sentences:
                if any(word in sent.lower() for word in ['because', 'since', 'due to', 'reason']):
                    return self._clean_sentence(sent)
        
        # Default: combine top sentences intelligently
        answer_parts = []
        for sent in sentences[:3]:
            cleaned = self._clean_sentence(sent)
            if cleaned and len(cleaned) > 20:
                # Avoid duplicate information
                if not any(self._is_similar(cleaned, existing) for existing in answer_parts):
                    answer_parts.append(cleaned)
        
        if not answer_parts:
            return self._clean_sentence(sentences[0])
        
        # Join sentences naturally
        if len(answer_parts) == 1:
            return answer_parts[0]
        elif len(answer_parts) == 2:
            return f"{answer_parts[0]} {answer_parts[1]}"
        else:
            return f"{answer_parts[0]} {answer_parts[1]} Additionally, {answer_parts[2].lower()}"
    
    def _clean_sentence(self, sentence: str) -> str:
        """Clean up a sentence for better readability."""
        # Remove page markers
        sentence = re.sub(r'\[Page \d+\]:\s*', '', sentence)
        
        # Remove extra whitespace
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        
        # Ensure proper ending
        if sentence and sentence[-1] not in '.!?':
            sentence += '.'
        
        return sentence
    
    def _is_similar(self, sent1: str, sent2: str) -> bool:
        """Check if two sentences are similar (to avoid repetition)."""
        words1 = set(sent1.lower().split())
        words2 = set(sent2.lower().split())
        
        if not words1 or not words2:
            return False
        
        # Calculate Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        similarity = intersection / union if union > 0 else 0
        return similarity > 0.6  # 60% similarity threshold
