// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.7.0;

import "../../node_modules/@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "../../node_modules/@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

interface ISimpleWrapperGatedUpgradeable {
    // @dev Get estimated value of vault position for an account
    function totalVaultBalance(address account) external view  returns (uint256);

    /// @dev Forward totalAssets from underlying vault
    function totalAssets() external view returns (uint256);

    function shareValue(uint256 numShares) external view returns (uint256);

    /// @dev Forward pricePerShare of underlying vault
    function pricePerShare() external view returns (uint256);

    function totalWrapperBalance(address account) external view returns (uint256);

    /// @dev Deposit specified amount of token in wrapper
    /// @dev A merkle proof can be supplied to verify inclusion in merkle guest list if this functionality is active
    function deposit(uint256 amount, bytes32[] calldata merkleProof) external returns (uint256);

    function withdraw(uint256 shares) external returns (uint256 withdrawn);

    /**
     * @notice Triggers an approval from owner to spends
     * @param owner The address to approve from
     * @param spender The address to be approved
     * @param amount The number of tokens that are approved (2^256-1 means infinite)
     * @param deadline The time at which to expire the signature
     * @param v The recovery byte of the signature
     * @param r Half of the ECDSA signature pair
     * @param s Half of the ECDSA signature pair
     */
    function permit(
        address owner,
        address spender,
        uint256 amount,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;

    // @dev Pausing is optimized for speed of action. The guardian is intended to be the option with the least friction, though manager or affiliate can pause as well.
    function pause() external;

    // @dev Unpausing requires a higher permission level than pausing, which is optimized for speed of action. The manager or affiliate can unpause
    function unpause() external;
}

