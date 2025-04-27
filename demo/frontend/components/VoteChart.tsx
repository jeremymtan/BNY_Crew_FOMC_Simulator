// frontend/components/VoteDisplay.tsx
"use client"
import React from 'react';
import { VoteData } from '../lib/types';

interface VoteDisplayProps {
    data: VoteData[];
}

const VoteDisplay: React.FC<VoteDisplayProps> = ({ data }) => {
    // State tracking
    const [currentData, setCurrentData] = React.useState<VoteData[]>(data);

    React.useEffect(() => {
        console.log("Vote data updated:", data); // Debug log
        setCurrentData(data);
    }, [data]);

    // Check if all votes are -999 (waiting)
    const allWaiting = currentData.every(item => {
        try {
            const voteStr = item.vote ? item.vote.replace(/%/g, '') : '-999';
            const voteValue = parseFloat(voteStr);
            return voteValue === -9999;
        } catch (e) {
            console.error("Error parsing vote data:", e);
            return true;
        }
    });

    // If all are waiting (-999), show waiting message
    if (allWaiting) {
        return (
            <div className="w-full">
                <h2 className="text-lg font-bold mb-3">FOMC Committee Votes</h2>
                <div className="p-4 bg-gray-50 border border-gray-200 rounded text-gray-500">
                    Waiting for committee members to cast their votes...
                </div>
            </div>
        );
    }

    return (
        <div className="w-full">
            <h2 className="text-lg font-bold mb-3">FOMC Committee Votes</h2>
            <div className="space-y-3">
                {currentData.map((item, index) => {
                    // Skip members who haven't voted yet (-999)
                    if (item.vote?.includes('-9999')) return null;

                    return (
                        <div
                            key={`${item.member}-${index}`}
                            className="p-3 rounded bg-gray-50"
                        >
                            <div className="font-bold">{item.member}</div>
                            <div className="mt-1">
                                <span className="font-medium">
                                    {item.policy_vote}
                                </span>
                            </div>
                            {item.prediction && item.prediction !== "0.00%" && item.prediction !== "0%" && item.prediction !== "-999%" && (
                                <div className="text-sm text-gray-600 mt-1">
                                    Prediction for next year: {item.prediction}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default VoteDisplay;