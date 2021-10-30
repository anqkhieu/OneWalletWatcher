"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class GapFillFailedError extends Error {
    constructor(from, to, publisherId, msgChainId, nbTrials) {
        super(`Failed to fill gap between ${from.serialize()} and ${to.serialize()}`
            + ` for ${publisherId}-${msgChainId} after ${nbTrials} trials`);
        this.from = from;
        this.to = to;
        this.publisherId = publisherId;
        this.msgChainId = msgChainId;
    }
}
exports.default = GapFillFailedError;
//# sourceMappingURL=GapFillFailedError.js.map